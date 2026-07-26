% --------------------------------------------------------------------------- %
% LaTeX Class File
% Author: IRoM LAB
% Version: 1.0
% Inspired by the META latex template
% --------------------------------------------------------------------------- %

% --------------------------------------------------------------------------- %

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{iromlab}
\LoadClassWithOptions{article}

% --------------------------------------------------------------------------- %
% Layout %

\RequirePackage[top=2.25cm, bottom=2.5cm, left=2.5cm, right=2.5cm, columnsep=0.65cm]{geometry}

% --------------------------------------------------------------------------- %
% Packages %
% \RequirePackage[T1]{fontenc}
% \RequirePackage[utf8]{inputenc}
\RequirePackage[latin, english]{babel}
\RequirePackage{multicol}
\RequirePackage{amsmath, amsfonts, amssymb, amsthm}
\RequirePackage{enumerate}
\RequirePackage[inline]{enumitem}
\RequirePackage{mathtools}
\RequirePackage{graphicx}
\RequirePackage{setspace}
\RequirePackage{longtable,tabularx}
\RequirePackage{parskip}
\RequirePackage{placeins} 
\RequirePackage{hyphenat}
\RequirePackage{float}
\RequirePackage{multirow}
\RequirePackage{bbm}
\RequirePackage[table,dvipsnames]{xcolor}
\RequirePackage{threeparttable}
\RequirePackage{balance}
\RequirePackage[ruled,algo2e]{algorithm2e}
\RequirePackage{algpseudocode}
\RequirePackage{adjustbox}
\RequirePackage{booktabs}
\RequirePackage{bm}
\RequirePackage{etoolbox}
\RequirePackage{microtype}
% \RequirePackage{appendix}
% \RequirePackage[title]{appendix}
\RequirePackage{units}
\RequirePackage{xspace}
\RequirePackage[most]{tcolorbox}
\RequirePackage{caption}

% \DisableLigatures[f]{family=sf*} 


% --------------------------------------------------------------------------- %
% Packages %
\definecolor{irom_red}{HTML}{960001}
\definecolor{bgcolor}{HTML}{F6F6F6}


% --------------------------------------------------------------------------- %
% References %


\RequirePackage[pagebackref=true]{hyperref}
\RequirePackage[noabbrev,nameinlink]{cleveref} 
\hypersetup{
  colorlinks,
  linkcolor=irom_red,
  citecolor=irom_red,
  urlcolor=irom_red
}

\RequirePackage[square,numbers,sort&compress]{natbib}
\def\bibfont{\small}


% --------------------------------------------------------------------------- %
% Sections %

\RequirePackage{titlesec}
\titleformat*{\paragraph}{\itshape}
\titleformat*{\section}{\Large\sffamily\bfseries}
\titleformat*{\subsection}{\large\sffamily\bfseries}
\titleformat*{\subsubsection}{\normalsize\sffamily\bfseries}
\DeclareTextFontCommand{\textbf}{\bfseries\sffamily}

\RequirePackage{caption}
\DeclareCaptionLabelSeparator{custom}{}
\DeclareCaptionFormat{custom}{{\sffamily\textbf{#1 #2}} #3}
\captionsetup{singlelinecheck=false,format=custom,labelsep=custom,font=small}
\captionsetup[sub]{singlelinecheck=true,format=custom,labelsep=custom,font=small}



% --------------------------------------------------------------------------- %
% Title Page %

\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect 
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}

\newcommand\authorlist{}
\newcommand\authorformat[2][]{{\sffamily \bfseries #2$^{#1}$}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{{\normalsize $^{#1}$#2}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\contributionlist{}
\newcommand\contributionformat[2][]{{\small $^{#1}$#2}}
\newcommand\contribution[2][]{\addtolist[#1]{#2}{\contributionlist}{\contributionformat}{, }}

\newcommand\metadatalist{}
\newcommand\metadataformat[2][]{{\small {\sffamily \bfseries #1:} #2}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

\renewcommand{\abstract}[1]{\def\abstractlist{{ #1}}}
\newcommand{\email}[1]{\href{mailto:#1}{\texttt{#1}}}

\newcommand{\keywords}[1]{\def\keywordslist{{\small {\sffamily \bfseries \textcolor{black}{\textbf{Keywords:}} {\color{irom_red} #1}}}}}

\newcommand{\website}[2]{\def\websitelist{{\small {\sffamily \bfseries \textcolor{black}{\textbf{Website:}} \href{#1}{{\color{irom_red} #2}}}}}}

\newcommand{\code}[2]{\def\codelist{{\small {\sffamily \bfseries \textcolor{black}{\textbf{Code:}} \href{#1}{{\color{irom_red} #2}}}}}}

\renewcommand\date[1]{\metadata[Date]{#1}}
\newcommand\correspondence[1]{\metadata[Correspondence]{#1}}

\renewcommand{\title}[1]{\newcommand{\titlelist}{{\huge\sffamily\bfseries #1}}}

\newcommand{\beginappendix}{\appendix{\huge\sffamily Appendix\par}}


% --------
% %% keywords definition
% \def\keywords#1{%
%  \ifdefined\isaccepted \else
%     \textbf{Keywords:} #1%
%  \fi
%   \ifdefined\nohyperref\else\ifdefined\hypersetup
%     \hypersetup{pdfkeywords={#1}}
%   \fi\fi
% }

% --------------------------------------------------------------------------- %
% Titlebox %


\newcommand{\mymaketitle}{%
  \tcbset{enhanced,frame hidden}
  \tcbset{left=0.5cm}
  \tcbset{right=0.5cm}
  \tcbset{top=0.5cm}
  \tcbset{bottom=0.5cm}
  \tcbset{arc=10pt}
  \tcbset{boxrule=0.0pt}
  \tcbset{colback=bgcolor}
  \tcbset{before skip=0pt}
  \tcbset{grow to left by=1.5pt}
  \tcbset{grow to right by=1.5pt}
  \tcbset{overlay={\node[
    anchor=south east,
    at= (frame.south east),
    xshift=-0.5cm,
    yshift=0.4cm] {\includegraphics[width=2.5cm]{style/logo/irom-icon.png}};
    }}
  % 
  \begin{tcolorbox}
    \setlength{\parindent}{0cm}
    \setlength{\parskip}{0.5cm}
    {
      \setlength{\parskip}{0cm}
      \raggedright
      \nohyphens
      %
      {
        \setstretch{1.818}
        \titlelist\par
      }
      \vskip 0.3cm
      %
      \authorlist\par
      \vskip 0.2cm
      %
      \affiliationlist\par
      %
      \contributionlist\par
      \vskip -0.1cm
    }
    %
    \abstractlist\par
    %
    \vskip -0.25cm
    %
    \ifcsdef{keywordslist}{\keywordslist\par}{}
    %
    \vskip -0.3cm
    %
    \ifcsdef{websitelist}{\websitelist\par}{}
    %
    \vskip -0.25cm
    %
    \ifcsdef{codelist}{\codelist\par}{}
    %
    \vskip -0.25cm
    %
    {
      \setlength{\parskip}{0cm}
      \ifdefempty{\metadatalist}{\vspace*{0.65cm}}{\metadatalist\par}
    }
  \end{tcolorbox}
  \tcbset{reset}
  \FloatBarrier
}

\if@twocolumn%
\renewcommand{\maketitle}{
\twocolumn[%
  \mymaketitle
  \vskip 0.38cm
]
}%
\else%
\renewcommand{\maketitle}{
  \mymaketitle
}%
\fi
