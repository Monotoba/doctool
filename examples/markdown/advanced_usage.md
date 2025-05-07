# Advanced Usage

This section covers advanced features and techniques for using the Document Conversion Tool.

## Custom Styling

You can customize the appearance of your HTML and PDF documents by providing a CSS file:

```bash
python src/docconvert.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --css ./styles/custom.css
```

In your job file:

```yaml
options:
  css: ./styles/custom.css
```

## Image Handling

The Document Conversion Tool supports embedding images in your documents or linking to them:

```bash
# Embed images in the output document
python src/docconvert.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --embed-images
```

In your job file:

```yaml
options:
  images:
    embed: true
    formats: ["jpg", "png", "webp", "svg"]
```

## Table of Contents

You can automatically generate a table of contents for your documents:

```bash
python src/docconvert.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --toc
```

In your job file:

```yaml
options:
  toc: true
```

## Document Combination

You can combine multiple documents into a single file:

```bash
python src/docconvert.py --combine --input-dir ./docs --output-file ./combined.pdf --from md --to pdf --files intro.md chapter1.md chapter2.md
```

In your job file:

```yaml
documents:
  - title: "Introduction"
    file: intro.md
  - title: "Chapter 1"
    file: chapter1.md
  - title: "Chapter 2"
    file: chapter2.md
    
combine:
  enabled: true
  output_file: combined.pdf
```

## Metadata

You can add metadata to your documents:

```yaml
combine:
  enabled: true
  output_file: combined.pdf
  metadata:
    title: "Document Title"
    author: "Author Name"
    subject: "Document Subject"
    keywords: "keyword1, keyword2, keyword3"
```

## Conversion Paths

The Document Conversion Tool supports various conversion paths:

- Markdown → HTML
- Markdown → PDF (via HTML)
- Markdown → OpenDocument
- HTML → PDF
- HTML → Markdown
- HTML → OpenDocument
- PDF → HTML (if feasible)
- PDF → Markdown (if feasible)
- PDF → OpenDocument
- OpenDocument → HTML
- OpenDocument → Markdown
- OpenDocument → PDF

## Tips and Tricks

### Incremental Conversion

For large documentation projects, you can use the tool to convert only the files that have changed:

```yaml
options:
  incremental: true
```

### Parallel Processing

For faster conversion of multiple files, you can enable parallel processing:

```yaml
options:
  parallel: true
  max_workers: 4  # Number of parallel workers
```

### Custom Templates

You can use custom templates for HTML output:

```yaml
options:
  template: ./templates/custom_template.html
```