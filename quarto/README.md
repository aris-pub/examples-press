# Iris Analysis Example

An interactive data science paper analyzing the classic Iris dataset using Python and Plotly visualizations, created with Quarto.

## About This Example

This example demonstrates computational research documents that combine code, narrative text, and interactive visualizations. The paper explores species clustering in the Iris dataset through petal and sepal measurements.

## Tools Required

- **Quarto**: Scientific publishing system
- **Python**: With data science packages (numpy, pandas, plotly, scikit-learn)

### Installation

**macOS:**
```bash
brew install quarto
```

**Windows:**
- Download the installer from [quarto.org/docs/get-started](https://quarto.org/docs/get-started/)

**Linux:**
- Download from [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) or use your distribution's package manager

Python dependencies are specified in the `.qmd` file and will be automatically managed by Quarto.

## Building

To generate the HTML output from the Quarto document:

```bash
quarto render iris_analysis.qmd
```

### What This Does

- Executes Python code blocks in `iris_analysis.qmd`
- Generates interactive Plotly visualizations
- Combines code, output, and narrative into a single HTML document
- Embeds all resources (JavaScript, CSS) for standalone viewing

## Files

- `iris_analysis.qmd` - Source file in Quarto Markdown format
- `iris_analysis.html` - Built HTML output with embedded visualizations

## Why This Matters

Quarto enables reproducible research by combining analysis code with narrative explanation. The interactive visualizations allow readers to explore data patterns directly in the browser, making computational research more accessible and transparent.
