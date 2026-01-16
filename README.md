# Examples Press

Example research scrolls for [Scroll Press](https://github.com/leotrs/press).

## About Scroll Press

Scroll Press is a modern preprint server for interactive, HTML-native research
documents. Unlike traditional preprint servers that primarily host PDFs, Press accepts
self-contained HTML files that can include interactive visualizations, executable code,
and dynamic elements. This enables researchers to share richer, more engaging scientific
communication.

This repository demonstrates how to use popular authoring tools to generate the single
self-contained HTML files that Press requires. Each example shows a complete workflow
from source document to publishable HTML output.

## Examples

1. **Typst** - Mathematical paper with Pandoc conversion
2. **Quarto** - Interactive data science with Python
3. **RSM** - Physics paper with embedded widget
4. **Jupyter** - Algorithms paper from Jupyter Notebook

Each example is in its own directory with a dedicated README containing:
- Overview of what the example demonstrates
- Tools required and installation instructions
- Exact build command to generate the HTML output
- Explanation of the build process

## Notes

- All HTML outputs are self-contained with embedded CSS/JavaScript
- Papers use different authoring tools to demonstrate Scroll Press's format flexibility
- Widget-based papers (RSM, Quarto) may require additional build steps for interactive elements
- Jupyter notebook demonstrates computational research workflow with executable code
