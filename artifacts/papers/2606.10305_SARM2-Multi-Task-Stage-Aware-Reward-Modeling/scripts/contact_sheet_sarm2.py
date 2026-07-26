import fitz
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
pdf=Path('artifacts/papers/2606.10305_SARM2-Multi-Task-Stage-Aware-Reward-Modeling/2606.10305_ko_translation_layout.pdf')
out=pdf.with_name('contact-sheet.png')
doc=fitz.open(pdf)
thumbs=[]
for i,p in enumerate(doc):
    pix=p.get_pixmap(matrix=fitz.Matrix(0.55,0.55),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    im.thumbnail((280,390))
    canvas=Image.new('RGB',(300,420),'white')
    canvas.paste(im,((300-im.width)//2,22))
    ImageDraw.Draw(canvas).text((8,4),f'p.{i+1}',fill='black')
    thumbs.append(canvas)
cols=4; rows=(len(thumbs)+cols-1)//cols
sheet=Image.new('RGB',(cols*300,rows*420),(220,220,220))
for i,im in enumerate(thumbs): sheet.paste(im,((i%cols)*300,(i//cols)*420))
sheet.save(out,optimize=True)
# deterministic QA stats
text_counts=[len(''.join(p.get_text().split())) for p in doc]
print({'pages':len(doc),'min_text_chars':min(text_counts),'min_page':text_counts.index(min(text_counts))+1,'blank_pages':[i+1 for i,x in enumerate(text_counts) if x<40],'contact_sheet':str(out),'size':pdf.stat().st_size})
