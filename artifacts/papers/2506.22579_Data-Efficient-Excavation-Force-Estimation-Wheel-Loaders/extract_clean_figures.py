#!/usr/bin/env python3
from pathlib import Path
import pymupdf as fitz

ROOT=Path(__file__).resolve().parent
pdf=fitz.open(ROOT/'original.pdf')
out=ROOT/'figures_clean'; out.mkdir(exist_ok=True)
# page (1-indexed), x1,y1,x2,y2 as page fractions. Captions intentionally excluded.
crops={
 1:(2, .53,.10,.96,.255),
 2:(3, .56,.08,.96,.265),
 3:(5, .05,.08,.50,.325),
 4:(7, .05,.08,.95,.285),
 5:(7, .58,.47,.95,.56),
 6:(8, .05,.50,.95,.59),
 7:(9, .05,.275,.48,.575),
 8:(10,.05,.07,.95,.285),
 9:(11,.05,.08,.95,.25),
10:(12,.05,.08,.95,.265),
}
for n,(pn,x1,y1,x2,y2) in crops.items():
 p=pdf[pn-1]; r=p.rect
 clip=fitz.Rect(r.x0+x1*r.width,r.y0+y1*r.height,r.x0+x2*r.width,r.y0+y2*r.height)
 pix=p.get_pixmap(matrix=fitz.Matrix(3,3),clip=clip,alpha=False)
 fn=out/f'fig-{n:02d}.png'; pix.save(fn)
 print(n,pn,clip,fn,pix.width,pix.height)
