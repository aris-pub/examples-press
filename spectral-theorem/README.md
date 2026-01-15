# Spectral Theorem Example

A mathematical paper demonstrating the spectral theorem for symmetric matrices, written in Typst and converted to HTML.

## About This Example

This example shows how to create mathematical research papers using Typst, a modern typesetting system designed as an alternative to LaTeX. The paper includes theorem-proof structures, mathematical equations, and academic formatting.

## Tools Required

- **Typst**: Modern typesetting system
- **Pandoc**: Document converter

### Installation

```bash
brew install typst pandoc
```

## Building

To generate the HTML output from the Typst source:

```bash
pandoc spectral_theorem.typ -s -o spectral_theorem.html --mathml
```

### What This Does

- Reads `spectral_theorem.typ` (Typst source)
- Converts it to standalone HTML (`-s` flag)
- Uses MathML for mathematical notation (`--mathml` flag)
- Outputs to `spectral_theorem.html`

## Files

- `spectral_theorem.typ` - Source file in Typst format
- `spectral_theorem.html` - Built HTML output (committed for convenience)

## Why This Matters

Typst provides a cleaner, more modern syntax than LaTeX while maintaining similar mathematical typesetting capabilities. Converting to HTML makes the content web-native and accessible through platforms like Scroll Press.
