# RSM Example

A physics paper exploring damped harmonic oscillators with an interactive simulation
widget, created using RSM (Readable Science Markup).

## About This Example

This example demonstrates interactive physics education with embedded simulations. The
paper examines three damping regimes (underdamped, critically damped, overdamped) and
includes a Bokeh widget for parameter exploration.

## Tools Required

- **RSM**: Readable Science Markup language
- **Python**: With rsm-markup package

### Installation

The `uv` package manager works on macOS, Windows, and Linux. If you don't have `uv`
installed, see
[docs.astral.sh/uv/getting-started/installation](https://docs.astral.sh/uv/getting-started/installation/).

**All platforms:**
```bash
uv add rsm-markup==0.4.1
```

## Building

To generate the HTML output from the RSM source:

```bash
uv run rsm-build damped_oscillators.rsm --css damped_oscillators.css --standalone -o damped_oscillators
```

### What This Does

- Reads `damped_oscillators.rsm` (RSM source markup)
- Applies styling from `damped_oscillators.css`
- Creates a standalone HTML file (`--standalone` flag)
- Embeds the pre-generated Bokeh widget (`damped_oscillator_widget.html`)
- Outputs to `damped_oscillators.html`

### Widget Generation

The interactive Bokeh widget is pre-generated using `generate_damped_widget.py`. To
regenerate it:

```bash
python generate_damped_widget.py
```

This creates `damped_oscillator_widget.html`, which gets embedded during the RSM build
process.

## Files

- `damped_oscillators.rsm` - Source file in RSM format
- `damped_oscillators.css` - Custom styling
- `generate_damped_widget.py` - Script to create the Bokeh widget
- `damped_oscillator_widget.html` - Pre-generated interactive widget
- `damped_oscillators.html` - Built HTML output with embedded widget

## Why This Matters

RSM enables authors to write physics and mathematics papers with lightweight markup
while embedding sophisticated interactive elements. The widget allows readers to
manipulate parameters and build intuition for physical systems directly in the browser.
