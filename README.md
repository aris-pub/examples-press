# Examples Press

Example research scrolls for [Scroll Press](https://github.com/leotrs/press). This repository contains sample academic papers in various formats to demonstrate Scroll Press's support for HTML-native research documents.

## Contents

1. **Spectral Theorem** (`spectral_theorem.typ`) - Typst + Pandoc
2. **Iris Analysis** (`iris_analysis.qmd`) - Quarto
3. **Damped Oscillators** (`damped_oscillators.rsm`) - RSM
4. **Graph Traversal** (`graph_traversal.ipynb`) - Jupyter Notebook

## Structure

```
.
├── scrolls.json                    # Metadata for all example scrolls
├── README.md                       # This file
├── *.html                          # Built HTML outputs
├── spectral_theorem.typ            # Typst source
├── iris_analysis.qmd               # Quarto source
├── damped_oscillators.rsm          # RSM source
├── damped_oscillators.css          # RSM styling
├── damped_oscillator_widget.html   # Pre-generated widget
├── generate_damped_widget.py       # Widget generator script
└── graph_traversal.ipynb           # Jupyter notebook source
```

## Prerequisites

Install the required tools:

```bash
# Pandoc (for Typst conversion)
brew install pandoc

# Typst (for mathematical papers)
brew install typst

# Quarto (for data science notebooks)
brew install quarto

# RSM (for interactive research manuscripts)
uv add rsm-markup==0.4.1
```

## Build Commands

### 1. Spectral Theorem (Typst → HTML via Pandoc)

```bash
pandoc spectral_theorem.typ -s -o spectral_theorem.html --mathml
```

**Source**: `spectral_theorem.typ`
**Output**: `spectral_theorem.html`
**Format**: Typst mathematical paper with theorem/proof environment

### 2. Iris Analysis (Quarto)

```bash
quarto render iris_analysis.qmd
```

**Source**: `iris_analysis.qmd`
**Output**: `iris_analysis.html`
**Format**: Quarto notebook with Python code, Plotly visualizations
**Requirements**: Python packages (numpy, pandas, plotly, scikit-learn)

### 3. Damped Oscillators (RSM)

```bash
uv run rsm-build damped_oscillators.rsm --css damped_oscillators.css --standalone -o damped_oscillators
```

**Source**: `damped_oscillators.rsm`
**Output**: `damped_oscillators.html`
**Format**: RSM interactive manuscript with Bokeh widgets
**Widget**: Pre-generated widget in `damped_oscillator_widget.html` (created by `generate_damped_widget.py`)

### 4. Graph Traversal (Jupyter Notebook)

```bash
quarto render graph_traversal.ipynb --to html --embed-resources --standalone
```

**Source**: `graph_traversal.ipynb`
**Output**: `graph_traversal.html`
**Format**: Jupyter Notebook with executable Python code, algorithms, visualizations
**Requirements**: Python with standard library (collections module)

## Rebuild All

To rebuild all seed papers:

```bash
# 1. Spectral Theorem
pandoc spectral_theorem.typ -s -o spectral_theorem.html --mathml

# 2. Iris Analysis (requires Python dependencies)
quarto render iris_analysis.qmd

# 3. Damped Oscillators
uv run rsm-build damped_oscillators.rsm --css damped_oscillators.css --standalone -o damped_oscillators

# 4. Graph Traversal
quarto render graph_traversal.ipynb --to html --embed-resources --standalone
```

## Usage with Scroll Press

This repository is designed to be used as a git submodule in the Scroll Press project. The `scrolls.json` file contains metadata for all example scrolls that the seeding script reads.

When using with Scroll Press, the `just seed` command will automatically clone this repository if it doesn't exist.

## Notes

- All HTML outputs are self-contained with embedded CSS/JavaScript
- Papers use different authoring tools to demonstrate Scroll Press's format flexibility
- Widget-based papers (RSM, Quarto) may require additional build steps for interactive elements
- Jupyter notebook demonstrates computational research workflow with executable code

## License

CC BY 4.0
