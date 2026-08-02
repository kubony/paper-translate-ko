# Technical investigation: public OpenReview forum GK4rznYwhn

## Bottom line

Recovered 15 public notes with exact current OpenReview note JSON: the submission, four Official Reviews, nine author comments/rebuttals, and one Meta Review. The current submission venue is exactly ICLR 2026 Poster. No separate public Decision note appeared in any recovered source; ICLR/OpenReview represents the outcome in the submission venue field, while independent ICLR 2026 datasets label it Accept (Poster).

The exact machine-readable inventory is openreview_target_notes_complete.json. A readable rendering of every content field is openreview_GK4rznYwhn_exact_inventory.md.

Because normal forum enumeration remains blocked by OpenReview's challenge, completeness cannot be proven through a direct forum= query. It is nevertheless strongly supported by the complete thread structure (four reviews, a response to every reviewer, five-part response to r9jt, one general response, and meta-review), the OpenReview search index, the archived forum page, and multiple independent ICLR 2026 datasets that agree on all four reviews and the result.

## Recovered note inventory

1. GK4rznYwhn — submission; venue ICLR 2026 Poster.
2. owkWXdMYqX — Official Review, Reviewer_GZFu; rating 8, confidence 4.
3. cGm4ePmZms — Official Review, Reviewer_EsMj; rating 4, confidence 4.
4. UaoMmYZOA2 — Official Review, Reviewer_r9jt; rating 4, confidence 5.
5. CE9elpUkqQ — Official Review, Reviewer_8eJ9; rating 8, confidence 4.
6. PO0sZejOgM — General Response: Details about the ground-truth data collection process and implementation for training the two systems.
7. iDkT81BkJU — Response to Reviewer 8eJ9.
8. Y8IFPe6uFo — Response to Reviewer r9jt (1/5).
9. QCoJEOrOu8 — Response to Reviewer r9jt (2/5).
10. giBp3AXwEw — Response to Reviewer r9jt (3/5).
11. E4p0JB67iZ — Response to Reviewer r9jt (4/5).
12. 8EOTRsXIrJ — Response to Reviewer r9jt (5/5).
13. gGJhC9UT7S — Response to Reviewer EsMj.
14. GV3br8fXO5 — Response to Reviewer GZFu.
15. WDsSgHhua9 — Meta Review by Area_Chair_g8At.

All are version 2 notes with readers including everyone and CC BY 4.0. Exact timestamps, invitations, signatures, readers/writers, and verbatim text are retained in the JSON.

## Meta-review recovered verbatim

The meta-review has three fields: summary, reviewer_concerns, and reviewer_scores. Its exact full wording is in both output files. In substance, it calls the contribution somewhat borderline, says rebuttal details and analyses improved the paper, recognizes positive overall scores, but finds the comparison and catastrophic-forgetting/generalization claims against prior dual-system architectures insufficiently substantiated.

## Decision evidence

- OpenReview submission content.venue.value: ICLR 2026 Poster.
- OpenReview archived page: displays ICLR 2026 Poster and an ICLR 2026 camera-ready BibTeX.
- JerMa88/ICLR_Peer_Reviews_2026: decision is Accept (Poster) on all four target review rows.
- weathon/iclr_2026: decision is Accept (Poster), gt_binary Accept, scores [8, 4, 4, 8].
- ai-conferences/ICLR2026: type Poster, submission_number 8310, arxiv_id 2512.08186.
- No separate Decision note ID/text was recovered. Searches for Accept, Poster, Accept (Poster), and decision-field variations did not return a target decision note.

## Routes attempted and HTTP/result evidence

### OpenReview website and documented API variants

- https://openreview.net/forum?id=GK4rznYwhn: HTTP 307 to /challenge?redirect=...; response was the Next.js challenge shell.
- www.openreview.net variants: HTTP 301 to openreview.net.
- api.openreview.net (v1) /notes with forum, id, or replyto: HTTP 403 ChallengeRequiredError.
- api2.openreview.net (v2) /notes with forum, id, or replyto: HTTP 403 ChallengeRequiredError.
- api2 /notes/edits?note.id=GK4rznYwhn: HTTP 403 ChallengeRequiredError.
- /revisions on API hosts: HTTP 404; the UI /revisions?id=... returned HTTP 200 and a 58,640-byte client shell, but its JavaScript calls getNoteById and /notes/edits, which are challenged. It contained no revision payload.
- /pdf and /attachment direct routes: HTTP 403.
- Jina-style public text proxy request for api2 /notes?forum=... returned only OpenReview's Verifying your browser page, not JSON.
- No CAPTCHA was solved, automated, bypassed, or circumvented.

### Official OpenReview Python client

Cloned the current public openreview/openreview-py repository and installed it. Both calls were exercised:

- openreview.Client(baseurl=https://api.openreview.net).get_notes(forum=...): OpenReviewException ChallengeRequiredError, HTTP 403.
- openreview.api.OpenReviewClient(baseurl=https://api2.openreview.net).get_notes(forum=...): same result.

This confirms the client does not expose another unauthenticated transport; it constructs the same challenged /notes?forum= request.

### Public OpenReview search endpoint — successful route

The public GET /notes/search endpoint remained accessible even when /notes was challenged. api2 returned HTTP 200 JSON. Search parameters exercised included term, content=all/metareview/decision, group=ICLR, source=all/reply, limit=1000, and details variants.

Key successful terms were DualVLN, GZFu, EsMj, 8eJ9, r9jt, self-directed, and view-adjustment. Target notes were selected only when id or forum exactly equaled GK4rznYwhn. This recovered the submission, all reviews, all author replies, the general response, and the meta-review. Multiword phrase queries often returned count 0, so reviewer aliases and distinctive single tokens were needed. v1 /notes/search returned legacy-format/older results and was not useful for this ICLR 2026 inventory; api2 was the productive index.

Raw search responses are preserved as openreview_search_*.json and openreview_search_alias_*.json.

### Static HTML and bootstrap data

- Direct forum HTML was challenge-gated and contained no paper/reply data.
- The unchallenged revisions page was only a Next.js shell.
- Its page chunk confirmed the exact client calls: getNoteById(id, details writable,forumContent, trash=true) and GET /notes/edits with note.id, sort=tcdate, details=writable,presentation,invitation, trash=true.
- The archived forum capture did include a Next.js bootstrap submission object and rendered submission metadata, but replies remained a client-side Loading placeholder.

### Web archives

- Wayback timemap returned one capture: timestamp 20260625180652, status 200, digest LSK577LA4AYVLCXQVTUM7WVPRSFPNMUN.
- Replaying with id_ returned HTTP 200, 173,830 bytes, correct paper title, author list, abstract, venue ICLR 2026 Poster, PDF/supplement paths, publication/modification dates, invitations, and BibTeX.
- The replay had no review/rebuttal/meta-review note IDs or text because replies were client-loaded.
- Wayback timemaps for OpenReview revisions and api/api2 notes/notes-edits exact URLs returned empty arrays.
- Common Crawl indexes CC-MAIN-2026-30, -25, -21, -17, and -12: exact URL queries returned 404 No Captures found; wildcard queries returned 404 or gateway 502/504 and yielded no records.
- Arquivo.pt full-text search for GK4rznYwhn: HTTP 200, estimated_nr_results 0.
- Memento Time Travel host did not resolve.

### Hugging Face / OpenReview review datasets

Dataset repository APIs and/or data files were inspected, not merely catalog descriptions.

- JerMa88/ICLR_Peer_Reviews_2026: queried converted Parquet directly with DuckDB over HTTPS; four exact paper_id rows. Preserves each api_raw_review with OpenReview note ID and exact fields; decision Accept (Poster).
- insomnia7/iclr2026_stats: one exact forum record with four reviews, note IDs, reviewer aliases, exact structured review fields, scores, dates, URLs, and CC BY 4.0.
- 3Liz22/iclr2026_real_reviews: four exact openreview_forum_id rows; combined review text and scores; meta_available=true.
- davidheineman/iclr-2026: streamed 195,851,799-byte JSON and found the exact forum record with all four reviews; no rebuttals/meta-review.
- weathon/iclr_2026: exact paper record with all four human reviews, scores [8,4,4,8], and decision Accept (Poster); no exact rebuttal/meta-review text.
- ai-conferences/ICLR2026: downloaded 5,923,100-byte Parquet; one exact row, type Poster, submission 8310, arXiv 2512.08186.
- Other catalog hits inspected included ICLR 2026 review/statistics/rebuttal-named datasets. MilaAI4Math/SoT_ICLR2026_Rebuttals contained model trainer-state loss files rather than paper rebuttal text. General OpenReview datasets last updated before the ICLR 2026 cycle were not applicable.
- Hugging Face datasets-server info/first-rows/parquet endpoints returned HTTP 200 for the above datasets. Attempts to use its filter endpoint with SQL-like where expressions returned HTTP 422 Parameter where contains errors or invalid symbols; direct Parquet/streaming reads were used instead.

### Crossref, Semantic Scholar, arXiv, DBLP, and ICLR program data

- Crossref works title query: HTTP 200 but no exact target registration/DOI among returned items; nearest results were unrelated.
- Semantic Scholar Graph request for ARXIV:2512.08186: HTTP 429 rate limit during the final evidence run, so it yielded no reviews or OpenReview thread data.
- arXiv export API id_list=2512.08186: HTTP 200, one exact v1 entry, title/authors/abstract, published 2025-12-09; no review content.
- DBLP publication search: HTTP 200, one exact CoRR record, DOI 10.48550/ARXIV.2512.08186; no review content.
- OpenAlex arXiv URL lookup: HTTP 404.
- ICLR program evidence was obtained through the current ai-conferences/ICLR2026 program dataset and the archived OpenReview page: Poster, submission 8310. These corroborate the outcome but do not hold review-thread text.

### GitHub/search discovery

- GitHub repository search for GK4rznYwhn and 2512.08186 returned no repository carrying the OpenReview thread. Issue search found paper references but no copied review inventory.
- Search-engine queries returned paper/arXiv/project mentions and snippets, not exact review or rebuttal text.

## Files and integrity

Primary deliverables:

- openreview_target_notes_complete.json — exact 15-note JSON inventory.
- openreview_GK4rznYwhn_exact_inventory.md — readable verbatim content rendering.
- openreview_http_route_evidence.json — direct route statuses and prefixes.
- scholarly_route_evidence.json — Crossref/S2/OpenAlex/DBLP/arXiv HTTP evidence.
- web_archive_route_evidence.json and wayback_timemap_evidence.json — archive checks.
- hf_JerMa_target.json and openreview_*_GK4rznYwhn.json — independent dataset extracts.
- wayback_capture_0.html — raw archived forum capture.
- openreview_revisions_page.html and openreview_revisions_chunk.js — revision UI evidence.

SHA-256:

- openreview_target_notes_complete.json: 8e7e7869dcf9941964d79c2309afc8d198bfa3024ffa355f1e91bdd1b90665fc
- openreview_GK4rznYwhn_exact_inventory.md: 07e798c0160a196c952c20defe3462fc825a7663dc49015b647edaed57170c33
