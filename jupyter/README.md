# Jupyter Example

An algorithms paper explaining BFS and DFS graph traversal with executable Python code
and visualizations, created from a Jupyter Notebook.

## About This Example

This example demonstrates how computational researchers can share executable code
alongside explanation. The notebook includes working implementations of breadth-first
search and depth-first search with step-by-step walkthroughs.

## Tools Required

- **Quarto**: For converting Jupyter notebooks to HTML (we use Quarto instead of
  nbconvert because it provides better handling of embedded resources and automatically
  creates self-contained HTML files with proper flags)
- **Python**: Standard library only (uses built-in collections module)

### Installation

**macOS:**
```bash
brew install quarto
```

**Windows:**
- Download the installer from
  [quarto.org/docs/get-started](https://quarto.org/docs/get-started/)

**Linux:**
- Download from [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) or
  use your distribution's package manager

No additional Python packages are required beyond the standard library.

## Building

To generate the HTML output from the Jupyter notebook:

```bash
quarto render graph_traversal.ipynb --to html --embed-resources --standalone
```

### What This Does

- Reads `graph_traversal.ipynb` (Jupyter notebook)
- Converts to HTML format (`--to html`)
- Embeds all resources like CSS and JavaScript (`--embed-resources`)
- Creates a standalone file that works without external dependencies (`--standalone`)
- Outputs to `graph_traversal.html`

## Files

- `graph_traversal.ipynb` - Source Jupyter notebook with code and markdown cells
- `graph_traversal.html` - Built HTML output with embedded code and results

## Why This Matters

Jupyter notebooks are the standard tool for computational research across data science,
machine learning, and scientific computing. Converting them to HTML makes the research
accessible to readers who don't have Jupyter installed, while preserving the code and
its output for full reproducibility.
