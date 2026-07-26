#!/usr/bin/env python3
"""수집한 미디어 자산을 Google Cloud Storage로 미러링하고 매니페스트에 기록한다.

사용법:
    python3 mirror_assets_gcs.py <작업폴더> --bucket <bucket-name> [--prefix paper-translate-ko]
        [--public] [--prune-over-mib 25] [--dry-run]

왜 필요한가:
    영상은 논문 PDF보다 훨씬 크다. 웹사이트 아카이브 한 건이 수 GB가 되기도 해서
    Git LFS 무료 한도(1 GiB)를 금방 넘긴다. 큰 자산은 GCS에 두고 저장소에는
    매니페스트·썸네일·작은 파일만 남기면, 링크 추적성은 유지하면서 clone이 가벼워진다.

동작:
    1. <작업폴더>/assets/videos.json을 읽는다.
    2. `local`이 있는 자산을 `gs://<bucket>/<prefix>/<작업폴더명>/...`으로 업로드한다.
       (이미 같은 크기로 올라가 있으면 건너뛴다.)
    3. 각 자산에 `remote`(gs:// URI)와 `remote_url`(브라우저 링크)을 기록한다.
    4. --prune-over-mib 지정 시, 업로드가 확인된 자산 중 상한을 넘는 로컬 파일을
       지우고 `local`을 제거한다. 썸네일은 항상 로컬에 남긴다(문서에 삽입되므로).

`gcloud` CLI가 인증된 상태여야 한다(`gcloud auth login`).
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

PUBLIC_URL = "https://storage.googleapis.com/{bucket}/{path}"
PRIVATE_URL = "https://storage.cloud.google.com/{bucket}/{path}"


def gcloud() -> str:
    path = shutil.which("gcloud")
    if not path:
        print("[오류] gcloud CLI를 찾지 못했다. Google Cloud SDK를 설치하고 "
              "`gcloud auth login`으로 인증하라.")
        raise SystemExit(2)
    return path


def remote_sizes(bucket: str, prefix: str) -> dict[str, int]:
    """gs://bucket/prefix 아래 객체의 (경로 → 바이트)를 조회한다."""
    cmd = [gcloud(), "storage", "ls", "--recursive", "--long",
           f"gs://{bucket}/{prefix}/**"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sizes: dict[str, int] = {}
    if proc.returncode != 0:
        return sizes
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0].isdigit() and parts[-1].startswith("gs://"):
            uri = parts[-1]
            sizes[uri] = int(parts[0])
    return sizes


def upload(local: Path, uri: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"  [dry] {local} → {uri}")
        return True
    cmd = [gcloud(), "storage", "cp", str(local), uri]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  [fail] {local.name}: {proc.stderr.strip().splitlines()[-1:] or proc.stderr}")
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="미디어 자산을 GCS로 미러링한다.")
    ap.add_argument("workdir", help="작업 폴더 (assets/videos.json을 포함)")
    ap.add_argument("--bucket", required=True, help="GCS 버킷 이름 (gs:// 접두사 없이)")
    ap.add_argument("--prefix", default="paper-translate-ko", help="버킷 내 경로 접두사")
    ap.add_argument("--public", action="store_true",
                    help="버킷이 공개 읽기면 storage.googleapis.com 링크를 기록한다")
    ap.add_argument("--prune-over-mib", type=float, default=0,
                    help="업로드 확인 후 이 크기를 넘는 로컬 파일을 지운다(0이면 유지)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    workdir = Path(args.workdir).resolve()
    manifest_path = workdir / "assets" / "videos.json"
    if not manifest_path.exists():
        print(f"[오류] videos.json 없음: {manifest_path}")
        return 2
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    prefix = f"{args.prefix.strip('/')}/{workdir.name}"
    template = PUBLIC_URL if args.public else PRIVATE_URL
    existing = {} if args.dry_run else remote_sizes(args.bucket, prefix)

    uploaded = skipped = pruned = relinked = 0
    prune_bytes = int(args.prune_over_mib * 1024 * 1024)

    for asset in data.get("assets", []):
        local_rel = asset.get("local")
        if not local_rel or not (workdir / local_rel).exists():
            # 이미 올리고 로컬을 정리한 자산 — 링크 형식(공개/비공개)만 갱신한다.
            if asset.get("remote", "").startswith(f"gs://{args.bucket}/"):
                object_path = asset["remote"].split(f"gs://{args.bucket}/", 1)[1]
                asset["remote_url"] = template.format(bucket=args.bucket, path=object_path)
                relinked += 1
            continue
        local = workdir / local_rel
        # assets/videos/foo.mp4 → <prefix>/videos/foo.mp4
        rel = Path(local_rel)
        rel = rel.relative_to("assets") if rel.parts[0] == "assets" else rel
        object_path = f"{prefix}/{rel.as_posix()}"
        uri = f"gs://{args.bucket}/{object_path}"

        if existing.get(uri) == local.stat().st_size:
            skipped += 1
        elif upload(local, uri, args.dry_run):
            uploaded += 1
            print(f"  [ok] {local.stat().st_size / 1024 / 1024:6.1f}MB → {uri}")
        else:
            continue

        asset["remote"] = uri
        asset["remote_url"] = template.format(bucket=args.bucket, path=object_path)

        if prune_bytes and not args.dry_run and local.stat().st_size > prune_bytes:
            local.unlink()
            asset.pop("local", None)
            pruned += 1

    if not args.dry_run:
        manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    print(f"\n업로드 {uploaded}개, 기존 동일 {skipped}개"
          + (f", 로컬 정리 {pruned}개" if pruned else "")
          + (f", 링크 갱신 {relinked}개" if relinked else ""))
    print(f"매니페스트: {manifest_path}")
    if not args.public:
        print("비공개 버킷 링크(storage.cloud.google.com)는 접근 권한이 있는 계정에서만 열린다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
