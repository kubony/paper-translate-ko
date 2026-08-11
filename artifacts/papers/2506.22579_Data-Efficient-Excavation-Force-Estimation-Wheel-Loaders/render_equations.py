#!/usr/bin/env python3
from pathlib import Path
import subprocess, tempfile, shutil

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'equations'; OUT.mkdir(exist_ok=True)

EQUATIONS=[
r"F_i=d_i^2w\gamma gN_{\gamma,i}+Cwd_iN_{c,i}+C_awd_iN_{a,i}+W_{\mathrm{load},i}N_{q,i}",
r"N_{\gamma,i}=\frac{(\cot\beta_i-\tan\alpha)[\cos\alpha+\sin\alpha\cot(\beta_i+\phi)]}{2[\cos(\rho_i+\delta)+\sin(\rho_i+\delta)\cot(\beta_i+\phi)]}",
r"N_{c,i}=\frac{1+\cot\beta_i\cot(\beta_i+\phi)}{\cos(\rho_i+\delta)+\sin(\rho_i+\delta)\cot(\beta_i+\phi)}",
r"N_{a,i}=\frac{1-\cot\rho_i\cot(\beta_i+\phi)}{\cos(\rho_i+\delta)+\sin(\rho_i+\delta)\cot(\beta_i+\phi)}",
r"N_{q,i}=\frac{\cos\alpha+\sin\alpha\cot(\beta_i+\phi)}{\cos(\rho_i+\delta)+\sin(\rho_i+\delta)\cot(\beta_i+\phi)}",
r"\cos\alpha+\sin\alpha\cot(\beta_i+\phi)=\frac{\sin(\alpha+\beta_i+\phi)}{\sin(\beta_i+\phi)}",
r"\cos(\rho_i+\delta)+\sin(\rho_i+\delta)\cot(\beta_i+\phi)=\frac{\sin(\rho_i+\delta+\beta_i+\phi)}{\sin(\beta_i+\phi)}",
r"N_{\gamma,i}=\frac{(\cot\beta_i-\tan\alpha)\sin(\alpha+\beta_i+\phi)}{2\sin(\rho_i+\delta+\beta_i+\phi)}",
r"\cot\beta_i-\tan\alpha=\frac{\cos(\alpha+\beta_i)}{\cos\alpha\cos\beta_i}",
r"N_{\gamma,i}=\frac{\cos(\alpha+\beta_i)\sin(\alpha+\beta_i+\phi)}{2\cos\alpha\sin\beta_i\sin(\rho_i+\delta+\beta_i+\phi)}",
r"N_{c,i}=\frac{\cos\phi}{\sin\beta_i\sin(\rho_i+\delta+\beta_i+\phi)}",
r"N_{a,i}=-\frac{\cos(\rho_i+\beta_i+\phi)\sin(\beta_i+\phi)}{\sin\rho_i\sin(\beta_i+\phi)\sin(\rho_i+\delta+\beta_i+\phi)}",
r"N_{q,i}=\frac{\sin(\alpha+\beta_i+\phi)}{\sin(\rho_i+\delta+\beta_i+\phi)}",
r"\beta_i>\varepsilon_1,\qquad \left|\rho_i+\delta+\beta_i+\phi-\pi\right|>\varepsilon_2",
r"P_i=\left(\frac{k_c}{b}+k_\phi\right)d_i^n",
r"F_i^T=wbP_i+F_i\sin\delta+C_awL_{t,i}",
r"F_i^N=F_i\cos\delta",
r"\boldsymbol{\theta}=\begin{bmatrix}\gamma&C&C_a&\phi&\delta&k_c&k_\phi&n\end{bmatrix}^{\!T}",
r"\begin{alignedat}{3}\min_{\boldsymbol{\theta}}\quad J_{\boldsymbol{\theta}}&=\lambda\sum_{i=1}^{N}(F_{\mathrm{obs},i}^{T}-F_i^{T})^2 +(1-\lambda)\sum_{i=1}^{N}(F_{\mathrm{obs},i}^{N}-F_i^{N})^2 &&\quad &(19\mathrm{a})\\ \text{s.t.}\quad F_i^{T}&=wbP_i+F_i\sin\delta+C_awL_{t,i} && &(19\mathrm{b})\\ F_i^{N}&=F_i\cos\delta && &(19\mathrm{c})\\ P_i&=\left(\frac{k_c}{b}+k_\phi\right)d_i^n && &(19\mathrm{d})\\ F_i&=d_i^2w\gamma gN_{\gamma,i}+Cwd_iN_{c,i}+C_awd_iN_{a,i}+W_{\mathrm{load}}N_{q,i} && &(19\mathrm{e})\\ N_{\gamma,i}&=f_\gamma(\alpha,\beta_i,\phi,\rho_i,\delta) && &(19\mathrm{f})\\ N_{c,i}&=f_c(\beta_i,\phi,\rho_i,\delta) && &(19\mathrm{g})\\ N_{a,i}&=f_a(\beta_i,\phi,\rho_i,\delta) && &(19\mathrm{h})\\ N_{q,i}&=f_q(\alpha,\beta_i,\phi,\rho_i,\delta),\quad i=1,\ldots,N && &(19\mathrm{i})\\ \boldsymbol{\theta}_{\min}&\leq\boldsymbol{\theta}\leq\boldsymbol{\theta}_{\max} && &(19\mathrm{j})\end{alignedat}",
r"F_{\mathrm{obs}}^N=F\cos\delta,\qquad F_{\mathrm{obs}}=\frac{F_{\mathrm{obs}}^N}{\cos\delta}",
r"F^T=wb\left(\frac{k_c}{b}+k_\phi\right)d^n+F_{\mathrm{obs}}^N\tan\delta+C_awL_t",
r"\boldsymbol{\theta}_1=\begin{bmatrix}C_a&\delta&k_c&k_\phi&n\end{bmatrix}^{T}",
r"\begin{alignedat}{3}\min_{\boldsymbol{\theta}_1}\quad J_{\boldsymbol{\theta}_1}^{1}&=\sum_{i=1}^{N}(F_{\mathrm{obs},i}^{T}-F_i^{T})^2 &&\quad &(23\mathrm{a})\\ \text{s.t.}\quad F_i^{T}&=wb\left(\frac{k_c}{b}+k_\phi\right)d_i^n+F_{\mathrm{obs},i}^{N}\tan\delta+C_awL_{t,i},\quad i=1,\ldots,N && &(23\mathrm{b})\\ \boldsymbol{\theta}_{1,\min}&\leq\boldsymbol{\theta}_1\leq\boldsymbol{\theta}_{1,\max} && &(23\mathrm{c})\end{alignedat}",
r"\boldsymbol{\theta}_1^*=\begin{bmatrix}C_a^*&\delta^*&k_c^*&k_\phi^*&n^*\end{bmatrix}^{T}",
r"F_{\mathrm{obs}}=\frac{F_{\mathrm{obs}}^N}{\cos\delta^*}",
r"\boldsymbol{\theta}_2=\begin{bmatrix}\gamma&C&\phi\end{bmatrix}^{T}",
r"\begin{alignedat}{3}\min_{\boldsymbol{\theta}_2}\quad J_{\boldsymbol{\theta}_2}&=\sum_{i=1}^{N}(F_{\mathrm{obs},i}-F_i)^2 &&\quad &(27\mathrm{a})\\ \text{s.t.}\quad F_i&=d_i^2w\gamma gN_{\gamma,i}+Cwd_iN_{c,i}+C_a^*wd_iN_{a,i}+W_{\mathrm{load}}N_{q,i} && &(27\mathrm{b})\\ N_{\gamma,i}&=f_\gamma(\alpha,\beta_i,\phi,\rho_i,\delta^*) && &(27\mathrm{c})\\ N_{c,i}&=f_c(\beta_i,\phi,\rho_i,\delta^*) && &(27\mathrm{d})\\ N_{a,i}&=f_a(\beta_i,\phi,\rho_i,\delta^*) && &(27\mathrm{e})\\ N_{q,i}&=f_q(\alpha,\beta_i,\phi,\rho_i,\delta^*),\quad i=1,\ldots,N && &(27\mathrm{f})\\ \boldsymbol{\theta}_{2,\min}&\leq\boldsymbol{\theta}_2\leq\boldsymbol{\theta}_{2,\max} && &(27\mathrm{g})\end{alignedat}",
r"\boldsymbol{\theta}_3=\begin{bmatrix}k_c&k_\phi&n\end{bmatrix}^{T}",
]

WIDE={19,23,27}

def render(n,eq):
    tex=rf'''\documentclass[border=3pt]{{standalone}}
\usepackage{{amsmath,amssymb,bm}}
\begin{{document}}
\begin{{minipage}}{{{18 if n in WIDE else 8.2}cm}}
\centering
$\displaystyle {eq}$
\end{{minipage}}
\end{{document}}
'''
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); (td/'eq.tex').write_text(tex)
        proc=subprocess.run(['latex','-interaction=nonstopmode','-halt-on-error','eq.tex'],cwd=td,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if proc.returncode:
            print(f'LaTeX failed for equation {n}:\n{proc.stdout}')
            raise subprocess.CalledProcessError(proc.returncode,proc.args)
        subprocess.run(['dvisvgm','--no-fonts','--exact','--bbox=preview','-o','eq.svg','eq.dvi'],cwd=td,check=True,stdout=subprocess.DEVNULL)
        shutil.copy2(td/'eq.svg',OUT/f'eq-{n:02d}.svg')

for i,eq in enumerate(EQUATIONS,1):
    render(i,eq)
print(f'rendered {len(EQUATIONS)} equations to {OUT}')
