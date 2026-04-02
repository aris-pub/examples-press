# Zip Upload Example: Quarto-Style Output

Demonstrates uploading a Quarto-style HTML output with a `_files/` directory structure. This is the pattern produced by `quarto render` with `self-contained: false`.

## Structure

```
zip-quarto-style/
  analysis.html                          <- entry point (auto-detected)
  analysis_files/
    libs/
      quarto.css                         <- framework stylesheet
      quarto.js                          <- framework script
    figure-html/
      conductivity-plot.svg              <- generated figure
```

## How to upload

Zip the contents and upload:

```bash
cd zip-quarto-style
zip -r ../zip-quarto-style.zip .
```

Press will auto-detect `analysis.html` as the entry point since it is the only HTML file at the root level. The `analysis_files/` directory and all its contents are preserved with their relative paths.

## Why this matters

Many Quarto users render with `self-contained: false` (the default) because self-contained mode can fail with large interactive plots or complex JavaScript libraries. This zip upload pattern lets them upload Quarto output directly without conversion.
