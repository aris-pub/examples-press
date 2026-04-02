# Examples Press

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Example research scrolls for [Scroll Press](https://github.com/aris-pub/press).

## About Scroll Press

Scroll Press is a modern preprint server for interactive, HTML-native research
documents. Unlike traditional preprint servers that primarily host PDFs, Press accepts
self-contained HTML files that can include interactive visualizations, executable code,
and dynamic elements. This enables researchers to share richer, more engaging scientific
communication.

This repository demonstrates how to use popular authoring tools to generate HTML for
Press. You can upload a single self-contained HTML file, or a zip archive with your HTML
and its assets (stylesheets, scripts, images, data files).

## Examples

### Single HTML File

1. **Typst** - Mathematical paper with Pandoc conversion
2. **Quarto** - Interactive data science with Python (self-contained)
3. **RSM** - Physics paper with embedded widget
4. **Jupyter** - Algorithms paper from Jupyter Notebook

### Zip Archive

5. **zip-simple** - Paper with separate CSS, JS, and SVG image
6. **zip-quarto-style** - Quarto-style output with `_files/` directory structure

Each example is in its own directory with a dedicated README containing:
- Overview of what the example demonstrates
- Tools required and installation instructions
- Exact build command to generate the output
- How to upload (single file or zip)

## Uploading a Zip

If your paper has external assets (images, CSS, JavaScript, data files), put everything
in a folder and zip it:

```bash
cd my-paper-folder
zip -r ../my-paper.zip .
```

Upload the zip on Press. The entry point HTML file is auto-detected. If there are
multiple HTML files, you can select the correct one.

**Allowed file types:** HTML, CSS, JavaScript, images (PNG, JPG, GIF, WebP, SVG), fonts
(WOFF, WOFF2, TTF, OTF), and data files (JSON, CSV, TSV, TXT). Maximum 50MB.

## Notes

- Single HTML uploads work as before -- all CSS/JS inlined in one file
- Zip uploads preserve directory structure and relative paths
- Papers use different authoring tools to demonstrate Press's format flexibility
- Widget-based papers (RSM, Quarto) may require additional build steps for interactive elements
