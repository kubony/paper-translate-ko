import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_cross_references.py"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_cross_references", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE = r"""
\setcounter{figure}{1}
\begin{figure*}
\caption{Architecture}
\label{fig:arch}
\end{figure*}
See Fig.~\ref{fig:arch}.
\begin{figure}
\caption{Coaching}
\label{fig:air_fryer_coaching}
\end{figure}
See Fig.~\ref{fig:air_fryer_coaching} and Fig.~\ref{fig:arch}.
"""


def test_resolve_figure_numbers_honors_setcounter_and_source_order():
    mod = load_module()
    assert mod.resolve_figure_numbers(SOURCE) == {
        "fig:arch": 2,
        "fig:air_fryer_coaching": 3,
    }


def test_resolve_figure_numbers_does_not_capture_nonfigure_labels_after_custom_caption():
    mod = load_module()
    source = r"""
    \captionsetup{type=figure}
    \caption{Teaser}\label{fig:teaser}
    \section{Introduction}\label{sec:intro}
    \begin{equation}x=1\label{eq:x}\end{equation}
    """
    assert mod.resolve_figure_numbers(source) == {"fig:teaser": 1}


def test_validate_rejects_display_number_drift():
    mod = load_module()
    html = """
    <figure id="fig-2" data-source-label="fig:arch" data-figure="2"></figure>
    <figure id="fig-3" data-source-label="fig:air_fryer_coaching" data-figure="3"></figure>
    <p><a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a></p>
    <p><a class="xref" data-source-ref="fig:air_fryer_coaching" href="#fig-2">그림 2</a></p>
    <p><a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a></p>
    """
    errors = mod.validate_cross_references(SOURCE, html)
    assert any("fig:air_fryer_coaching" in error and "expected 3" in error for error in errors)


def test_validate_rejects_missing_or_extra_reference_occurrences():
    mod = load_module()
    html = """
    <figure id="fig-2" data-source-label="fig:arch" data-figure="2"></figure>
    <figure id="fig-3" data-source-label="fig:air_fryer_coaching" data-figure="3"></figure>
    <p><a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a></p>
    """
    errors = mod.validate_cross_references(SOURCE, html)
    assert any("reference occurrence mismatch" in error for error in errors)


def test_validate_accepts_exact_label_number_href_target_and_counts():
    mod = load_module()
    html = """
    <figure id="fig-2" data-source-label="fig:arch" data-figure="2"></figure>
    <figure id="fig-3" data-source-label="fig:air_fryer_coaching" data-figure="3"></figure>
    <p><a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a></p>
    <p><a class="xref" data-source-ref="fig:air_fryer_coaching" href="#fig-3">그림 3</a></p>
    <p><a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a></p>
    """
    assert mod.validate_cross_references(SOURCE, html) == []
