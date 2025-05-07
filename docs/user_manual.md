# Document Conversion Tool - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Command-Line Interface](#command-line-interface)
5. [Job Files](#job-files)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

## Introduction

The Document Conversion Tool is a flexible, general-purpose solution for converting between various document formats and optionally combining multiple documents into a single file. It supports Markdown, HTML, PDF, and OpenDocument formats, with a modular architecture that allows for easy extension to support additional formats in the future.

### Key Features

- **Format Conversion**: Convert between Markdown, HTML, PDF, and OpenDocument formats
- **Document Combination**: Combine multiple documents into a single file
- **Job File Support**: Use YAML or JSON job files for complex conversion tasks
- **Command-Line Interface**: Simple CLI for quick conversions
- **Custom Styling**: Apply custom CSS to HTML and PDF output
- **Image Handling**: Embed or link to images (JPEG, PNG, WebP, SVG)
- **Table of Contents**: Automatically generate a table of contents
- **Metadata Support**: Add title, author, and other metadata to documents

## Installation

### Prerequisites

- Python 3.8 or higher
- Required Python packages (installed automatically with pip)

### Installation Steps

1. Clone the repository or download the source code:

```bash
git clone https://github.com/yourusername/document-conversion-tool.git
cd document-conversion-tool
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Install development dependencies if you plan to contribute:

```bash
pip install -r requirements-dev.txt
```

## Basic Usage

The Document Conversion Tool can be used in two main ways:

1. **Command-Line Interface**: For quick, one-off conversions
2. **Job Files**: For more complex conversion tasks with multiple files and custom options

### Quick Start

Convert a Markdown file to HTML:

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.html --from md --to html
```

Convert a Markdown file to PDF:

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf
```

Convert all Markdown files in a directory to HTML:

```bash
python src/doctool.py --input-dir ./docs --output-dir ./html --from md --to html
```

Combine multiple PDF files:

```bash
python src/doctool.py --combine --input-dir ./pdfs --output-file ./combined.pdf --from pdf --to pdf --files file1.pdf file2.pdf file3.pdf
```

## Command-Line Interface

The Document Conversion Tool provides a comprehensive command-line interface with the following options:

### Basic Options

- `--input-file FILE`: Input file path
- `--input-dir DIR`: Input directory path
- `--output-file FILE`: Output file path
- `--output-dir DIR`: Output directory path
- `--from FORMAT`: Input format (md, html, pdf, odt)
- `--to FORMAT`: Output format (md, html, pdf, odt)

### Combination Options

- `--combine`: Enable document combination
- `--files FILE [FILE ...]`: List of files to combine (in order)

### Styling Options

- `--css FILE`: Custom CSS file for HTML/PDF output
- `--toc`: Generate table of contents
- `--embed-images`: Embed images in the output document

### Job File Options

- `--job-file FILE`: Path to YAML or JSON job file

### Help

- `--help`: Show help message and exit

## Job Files

For more complex conversion tasks, you can use job files in YAML or JSON format. Job files allow you to specify multiple input files, custom options, and metadata.

### YAML Job File Example

```yaml
# Basic configuration
input_dir: ./docs
output_dir: ./output
from_format: md
to_format: pdf

# Document list (for combining)
documents:
  - title: "Introduction"
    file: intro.md
  - title: "Getting Started"
    file: getting_started.md
  - title: "Advanced Usage"
    file: advanced_usage.md

# Combination settings
combine:
  enabled: true
  output_file: combined.pdf
  metadata:
    title: "Complete Documentation"
    author: "Your Name"
    subject: "User Guide"
    keywords: "documentation, guide, manual"

# Additional options
options:
  css: ./styles/custom.css
  toc: true
  embed_images: true
```

### JSON Job File Example

```json
{
  "input_dir": "./docs",
  "output_dir": "./output",
  "from_format": "md",
  "to_format": "pdf",
  "documents": [
    {
      "title": "Introduction",
      "file": "intro.md"
    },
    {
      "title": "Getting Started",
      "file": "getting_started.md"
    },
    {
      "title": "Advanced Usage",
      "file": "advanced_usage.md"
    }
  ],
  "combine": {
    "enabled": true,
    "output_file": "combined.pdf",
    "metadata": {
      "title": "Complete Documentation",
      "author": "Your Name",
      "subject": "User Guide",
      "keywords": "documentation, guide, manual"
    }
  },
  "options": {
    "css": "./styles/custom.css",
    "toc": true,
    "embed_images": true
  }
}
```

### Using Job Files

To use a job file:

```bash
python src/doctool.py --job-file ./examples/example_job.yaml
```

or

```bash
python src/doctool.py --job-file ./examples/example_job.json
```

## Advanced Features

### Custom Styling

You can customize the appearance of your HTML and PDF documents by providing a CSS file:

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --css ./styles/custom.css
```

### Image Handling

The Document Conversion Tool supports embedding images in your documents or linking to them:

```bash
# Embed images in the output document
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --embed-images
```

### Table of Contents

You can automatically generate a table of contents for your documents:

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --toc
```

### Document Combination

You can combine multiple documents into a single file:

```bash
python src/doctool.py --combine --input-dir ./docs --output-file ./combined.pdf --from md --to pdf --files intro.md chapter1.md chapter2.md
```

### Metadata

You can add metadata to your documents using a job file:

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

## Troubleshooting

### Common Issues

#### Missing Dependencies

If you encounter errors about missing dependencies, make sure you have installed all required packages:

```bash
pip install -r requirements.txt
```

#### File Not Found

If you get "File not found" errors, check that the paths in your command or job file are correct. Remember that relative paths are relative to the current working directory, not the location of the script.

#### Conversion Errors

If you encounter errors during conversion:

1. Check that the input file is valid and properly formatted
2. Ensure that the input and output formats are supported
3. Check for any special characters or elements that might cause issues

### Getting Help

If you continue to experience issues, please:

1. Check the project documentation
2. Look for similar issues in the project's issue tracker
3. Submit a new issue with a detailed description of the problem and steps to reproduce it

## Examples

### Basic Conversion Examples

#### Markdown to HTML

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.html --from md --to html
```

#### Markdown to PDF

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf
```

#### HTML to PDF

```bash
python src/doctool.py --input-file ./input.html --output-file ./output.pdf --from html --to pdf
```

#### Batch Conversion

```bash
python src/doctool.py --input-dir ./docs --output-dir ./html --from md --to html
```

### Advanced Examples

#### Custom Styling

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --css ./styles/custom.css
```

#### Embedding Images

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --embed-images
```

#### Table of Contents

```bash
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf --toc
```

#### Combining Documents

```bash
python src/doctool.py --combine --input-dir ./docs --output-file ./combined.pdf --from md --to pdf --files intro.md chapter1.md chapter2.md
```

#### Using a Job File

```bash
python src/doctool.py --job-file ./examples/example_job.yaml
```