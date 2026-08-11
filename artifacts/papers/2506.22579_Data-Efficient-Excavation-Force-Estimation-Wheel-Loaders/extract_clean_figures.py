#!/usr/bin/env python3
from pathlib import Path
import pymupdf as fitz

ROOT=Path(__file__).resolve().parent
pdf=fitz.open(ROOT/'original.pdf')
out=ROOT/'figures_clean'; out.mkdir(exist_ok=True)
# page (1-indexed), x1,y1,x2,y2 as page fractions. Captions intentionally excluded.
crops={
 1:(2, .510,.080,.950,.255),
 2:(3, .525,.080,.950,.260),
 3:(5, .055,.080,.460,.310),
 4:(7, .095,.085,.950,.295),
 5:(7, .500,.392,.930,.535),
 6:(8, .060,.375,.950,.575),
 7:(9, .060,.270,.465,.605),
 8:(10,.055,.080,.950,.285),
 9:(11,.105,.080,.950,.255),
10:(12,.090,.080,.950,.268),
}
for n,(pn,x1,y1,x2,y2) in crops.items():
 p=pdf[pn-1]; r=p.rect
 clip=fitz.Rect(r.x0+x1*r.width,r.y0+y1*r.height,r.x0+x2*r.width,r.y0+y2*r.height)
 pix=p.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,alpha=False)
 fn=out/f'fig-{n:02d}.png'; pix.save(fn)
 print(n,pn,clip,fn,pix.width,pix.height)
