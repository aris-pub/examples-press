# Examples Press

Example research scrolls for [Scroll Press](https://github.com/leotrs/press).

## About Scroll Press

Scroll Press is a modern preprint server for interactive, HTML-native research documents. Unlike traditional preprint servers that primarily host PDFs, Press accepts self-contained HTML files that can include interactive visualizations, executable code, and dynamic elements. This enables researchers to share richer, more engaging scientific communication.

This repository demonstrates how to use popular authoring tools to generate the single self-contained HTML files that Press requires. Each example shows a complete workflow from source document to publishable HTML output.

## Contents

1. **Typst** - Mathematical paper with Pandoc conversion
2. **Quarto** - Interactive data science with Python
3. **RSM** - Physics paper with embedded widget
4. **Jupyter** - Algorithms paper from Jupyter Notebook

## Structure

```
examples-press/
├── README.md                       # This file
├── scrolls.json                    # Metadata for all examples
│
├── typst/                          # Typst + Pandoc example
│   ├── README.md
│   ├── spectral_theorem.typ
│   └── spectral_theorem.html
│
├── quarto/                         # Quarto example
│   ├── README.md
│   ├── iris_analysis.qmd
│   └── iris_analysis.html
│
├── rsm/                            # RSM example
│   ├── README.md
│   ├── damped_oscillators.rsm
│   ├── damped_oscillators.css
│   ├── damped_oscillator_widget.html
│   ├── generate_damped_widget.py
│   └── damped_oscillators.html
│
└── jupyter/                        # Jupyter Notebook example
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

### 1. [Typst](typst/) - Typst + Pandoc

Mathematical paper with theorem-proof structures. Demonstrates how modern typesetting tools like Typst can produce web-native research documents.

**[View build instructions →](typst/README.md)**

### 2. [Quarto](quarto/) - Quarto

Interactive data science paper with Python code and Plotly visualizations. Shows how computational notebooks can become publishable research documents.

**[View build instructions →](quarto/README.md)**

### 3. [RSM](rsm/) - RSM

Physics paper with embedded Bokeh simulation widget. Illustrates how interactive elements can enhance understanding of physical systems.

**[View build instructions →](rsm/README.md)**

### 4. [Jupyter](jupyter/) - Jupyter Notebook

Algorithms paper with executable code and visualizations. Demonstrates the Jupyter-to-HTML workflow for reproducible computational research.

**[View build instructions →](jupyter/README.md)**

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
