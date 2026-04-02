# Zip Upload Example: Simple Multi-File Paper

A minimal example of a zip upload to Scroll Press: an HTML paper with separate CSS, JavaScript, and image files.

## Structure

```
zip-simple/
  index.html          <- entry point (auto-detected)
  styles/paper.css    <- external stylesheet
  scripts/table-sort.js <- sortable table columns
  images/prime-spiral.svg <- figure
```

## How to upload

Zip the contents of this directory and upload:

```bash
cd zip-simple
zip -r ../zip-simple.zip .
```

Then upload `zip-simple.zip` on Scroll Press. The entry point (`index.html`) will be auto-detected.
