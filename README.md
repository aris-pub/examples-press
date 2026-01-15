# Examples Press

Example research scrolls for [Scroll Press](https://github.com/leotrs/press). This repository contains sample academic papers in various formats to demonstrate Scroll Press's support for HTML-native research documents.

## Contents

1. **Spectral Theorem** (`spectral_theorem.typ`) - Typst + Pandoc
2. **Iris Analysis** (`iris_analysis.qmd`) - Quarto
3. **Damped Oscillators** (`damped_oscillators.rsm`) - RSM
4. **Graph Traversal** (`graph_traversal.ipynb`) - Jupyter Notebook

## Structure

```
examples-press/
├── README.md                       # This file
├── scrolls.json                    # Metadata for all examples
│
├── spectral-theorem/               # Typst + Pandoc example
│   ├── README.md
│   ├── spectral_theorem.typ
│   └── spectral_theorem.html
│
├── iris-analysis/                  # Quarto example
│   ├── README.md
│   ├── iris_analysis.qmd
│   └── iris_analysis.html
│
├── damped-oscillators/             # RSM example
│   ├── README.md
│   ├── damped_oscillators.rsm
│   ├── damped_oscillators.css
│   ├── damped_oscillator_widget.html
│   ├── generate_damped_widget.py
│   └── damped_oscillators.html
│
└── graph-traversal/                # Jupyter Notebook example
    ├── README.md
    ├── graph_traversal.ipynb
    └── graph_traversal.html
```

## Examples

Each example is in its own directory with a dedicated README containing:
- Overview of what the example demonstrates
- Tools required and installation instructions
- Exact build command to generate the HTML output
- Explanation of the build process

### 1. [Spectral Theorem](spectral-theorem/) - Typst + Pandoc

Mathematical paper with theorem-proof structures. Demonstrates how modern typesetting tools like Typst can produce web-native research documents.

**[View build instructions →](spectral-theorem/README.md)**

### 2. [Iris Analysis](iris-analysis/) - Quarto

Interactive data science paper with Python code and Plotly visualizations. Shows how computational notebooks can become publishable research documents.

**[View build instructions →](iris-analysis/README.md)**

### 3. [Damped Oscillators](damped-oscillators/) - RSM

Physics paper with embedded Bokeh simulation widget. Illustrates how interactive elements can enhance understanding of physical systems.

**[View build instructions →](damped-oscillators/README.md)**

### 4. [Graph Traversal](graph-traversal/) - Jupyter Notebook

Algorithms paper with executable code and visualizations. Demonstrates the Jupyter-to-HTML workflow for reproducible computational research.

**[View build instructions →](graph-traversal/README.md)**

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
