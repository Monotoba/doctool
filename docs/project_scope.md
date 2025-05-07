# Document Conversion Tool - Project Scope

### ECO: ECO-20250506-001

## Overview

This project aims to create a flexible, general-purpose document conversion tool that can convert between various document formats (Markdown, HTML, PDF, OpenDocument) and optionally combine multiple documents into a single file. The tool will support both simple command-line usage for quick conversions and job file-based usage for more complex conversion jobs.

## Current Implementation

The existing codebase provides basic functionality for:
1. Converting Markdown files to HTML
2. Converting HTML files to PDF
3. Combining multiple PDFs into a single document

However, the current implementation has several limitations:
- Fixed input/output directories (docs/ebook/markdown, docs/ebook/html, docs/ebook/pdf)
- Limited conversion paths (only MD→HTML→PDF→combined PDF)
- Hardcoded chapter order for PDF combination
- No direct conversion between certain formats (e.g., PDF to HTML)
- No job file support for complex conversion tasks

## Proposed Enhancements

### 1. Flexible Document Conversion

Support the following conversion paths:
- Markdown → HTML
- Markdown → PDF (via HTML)
- Markdown → OpenDocument (new)
- HTML → PDF
- HTML → Markdown (new)
- HTML → OpenDocument (new)
- PDF → HTML (new, if feasible)
- PDF → Markdown (new, if feasible)
- PDF → OpenDocument (new)
- OpenDocument → HTML (new)
- OpenDocument → Markdown (new)
- OpenDocument → PDF (new)

### 2. Command-Line Interface Improvements

Enhance the CLI to support:
- Specifying input and output directories
- Selecting conversion type
- Setting output format
- Controlling file naming
- Specifying custom CSS for HTML/PDF output
- Defining document order for combination
- Specifying a job file to use

Example usage:
```
# Convert all markdown files in input_dir to HTML in output_dir
python docconvert.py --input-dir ./input_dir --output-dir ./output_dir --from md --to html

# Convert a specific file
python docconvert.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf

# Combine multiple PDFs in order
python docconvert.py --combine --input-dir ./pdfs --output-file ./combined.pdf --files file1.pdf file2.pdf file3.pdf

# Use a job file
python docconvert.py --job-file ./my_conversion_job.yaml
```

### 3. Job File Support

Add support for both YAML and JSON job files to define complex conversion jobs. If no job file is specified and no command-line arguments are provided, the tool will search for a `.yaml` or `.json` file in the same directory and use that if found.

Example job file (YAML):
```yaml
input:
  directory: ./docs/source
  format: markdown
  
output:
  directory: ./docs/output
  format: pdf
  
options:
  css: ./styles/custom.css
  toc: true
  cover_page: ./cover.md
  images:
    embed: true  # Embed images in the output document
    formats: ["jpg", "png", "webp", "svg"]  # Supported image formats
  
documents:
  - title: "Introduction"
    file: intro.md
  - title: "Chapter 1: Getting Started"
    file: chapter1.md
  - title: "Chapter 2: Advanced Topics"
    file: chapter2.md
    
combine:
  enabled: true
  output_file: complete_manual.pdf
  metadata:
    title: "Complete User Manual"
    author: "Documentation Team"
```

Example job file (JSON):
```json
{
  "input": {
    "directory": "./docs/source",
    "format": "markdown"
  },
  "output": {
    "directory": "./docs/output",
    "format": "pdf"
  },
  "options": {
    "css": "./styles/custom.css",
    "toc": true,
    "cover_page": "./cover.md",
    "images": {
      "embed": true,
      "formats": ["jpg", "png", "webp", "svg"]
    }
  },
  "documents": [
    {
      "title": "Introduction",
      "file": "intro.md"
    },
    {
      "title": "Chapter 1: Getting Started",
      "file": "chapter1.md"
    },
    {
      "title": "Chapter 2: Advanced Topics",
      "file": "chapter2.md"
    }
  ],
  "combine": {
    "enabled": true,
    "output_file": "complete_manual.pdf",
    "metadata": {
      "title": "Complete User Manual",
      "author": "Documentation Team"
    }
  }
}
```

### 4. Additional Features

- **Table of Contents Generation**: Automatically generate a TOC for combined documents
- **Metadata Support**: Add title, author, date, etc. to generated documents
- **Custom Styling**: Support custom CSS for HTML and PDF output
- **Template Support**: Allow custom templates for HTML output
- **Image Handling**: Support for embedding or linking to images (JPEG, PNG, WebP, SVG)
- **Incremental Conversion**: Only convert files that have changed since last run
- **Parallel Processing**: Convert multiple files simultaneously for better performance
- **Plugin System**: Allow for extensibility with custom converters

## Technical Requirements

### Dependencies

- **Markdown Processing**: `markdown` (existing)
- **HTML to PDF**: `weasyprint` (existing)
- **PDF Manipulation**: `PyPDF2` (existing)
- **HTML to Markdown**: `html2text` (new)
- **PDF to HTML/Text**: `pdfminer.six` or similar (new, if implemented)
- **Configuration**: `pyyaml` and `json` (new)
- **OpenDocument Format**: `odfpy` or similar (new)
- **Image Processing**: `Pillow` (new)

### Architecture

The tool will follow a modular architecture:

1. **Core Module**: Central coordinator that handles command-line arguments, job file parsing, and orchestration
2. **Converter Modules**: Specialized modules for each conversion type (MD→HTML, HTML→PDF, etc.)
3. **Combiner Module**: Handles combining multiple documents
4. **Job Module**: Parses and validates job files (YAML/JSON)
5. **Image Module**: Handles image processing and embedding
6. **Utility Module**: Common functions used across the application

## Implementation Plan

### Phase 1: Job File Support and Refactoring
- Implement job file parsing (YAML/JSON)
- Refactor existing code to be more modular and flexible
- Abstract hardcoded paths and settings
- Implement auto-detection of job files in the current directory

### Phase 2: Command-Line Interface
- Implement enhanced CLI with argument parsing
- Support basic conversion operations via CLI
- Add support for specifying job files via CLI

### Phase 3: New Converters
- Implement HTML to Markdown conversion
- Implement OpenDocument format support
- Research and implement PDF to HTML/Markdown if feasible
- Add image handling capabilities

### Phase 4: Advanced Features
- Implement TOC generation
- Add metadata support
- Implement custom styling and templates
- Add incremental conversion

## Conclusion

This enhanced document conversion tool will provide a flexible, powerful solution for converting and combining documentation in various formats. It will be suitable for use in different documentation projects, supporting both simple one-off conversions via command line and complex documentation builds via job files. The tool's modular architecture will make it easy to extend with new formats and features in the future.
