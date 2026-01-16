# Typst Example

A mathematical paper demonstrating the spectral theorem for symmetric matrices, written
in Typst and converted to HTML.

## About This Example

This example shows how to create mathematical research papers using Typst, a modern
typesetting system designed as an alternative to LaTeX. The paper includes theorem-proof
structures, mathematical equations, and academic formatting.

## Tools Required

- **Typst**: Modern typesetting system
- **Pandoc**: Document converter (used because Typst's native HTML support is
  experimental at the time of writing)

### Installation

**macOS:**
```bash
brew install typst pandoc
```

**Windows:**
- Typst: Download from
  [github.com/typst/typst/releases](https://github.com/typst/typst/releases) or use
  `winget install --id Typst.Typst`
- Pandoc: Download from [pandoc.org/installing.html](https://pandoc.org/installing.html)
  or use `winget install --id JohnMacFarlane.Pandoc`

**Linux:**
- Typst: Download from
  [github.com/typst/typst/releases](https://github.com/typst/typst/releases) or install
  via package manager
- Pandoc: `sudo apt install pandoc` (Debian/Ubuntu) or use your distribution's package
  manager

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

Typst provides a cleaner, more modern syntax than LaTeX while maintaining similar
mathematical typesetting capabilities. Converting to HTML makes the content web-native
and accessible through platforms like Scroll Press.
