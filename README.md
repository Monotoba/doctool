# Document Conversion Tool

A flexible, general-purpose document conversion tool that can convert between various document formats (Markdown, HTML, PDF, OpenDocument) and optionally combine multiple documents into a single file.

## Features

- Convert between multiple document formats:
  - Markdown → HTML, PDF, OpenDocument
  - HTML → Markdown, PDF, OpenDocument
  - PDF → HTML, Markdown, OpenDocument
  - OpenDocument → HTML, Markdown, PDF
- Combine multiple documents into a single file
- Support for both command-line usage and job files (YAML/JSON)
- Custom styling with CSS
- Image handling (embedding or linking)
- Table of contents generation
- Metadata support

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:Monotoba/doctool.git
   cd doctool
   ```

2. Install dependencies:
   ```
   pip install markdown weasyprint PyPDF2 pyyaml html2text odfpy Pillow
   ```

## Usage

### Command-Line Usage

```bash
# Convert all markdown files in input_dir to HTML in output_dir
python src/doctool.py --input-dir ./input_dir --output-dir ./output_dir --from md --to html

# Convert a specific file
python src/doctool.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf

# Combine multiple PDFs in order
python src/doctool.py --combine --input-dir ./pdfs --output-file ./combined.pdf --from pdf --to pdf --files file1.pdf file2.pdf file3.pdf

# Use a job file
python src/doctool.py --job-file ./my_conversion_job.yaml
```

### Job File Usage

Create a YAML or JSON job file to define complex conversion jobs:

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
    embed: true
    formats: ["jpg", "png", "webp", "svg"]
  
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

## Project Structure

```
doctool/
├── src/
│   ├── docconvert/
│   │   ├── converters/
│   │   │   ├── markdown_to_html.py
│   │   │   ├── html_to_pdf.py
│   │   │   ├── html_to_markdown.py
│   │   │   └── pdf_combiner.py
│   │   ├── core/
│   │   │   └── converter.py
│   │   ├── job/
│   │   │   └── job_parser.py
│   │   ├── image/
│   │   │   └── image_handler.py
│   │   └── utils/
│   └── docconvert.py
├── docs/
│   ├── project_scope.md
│   └── summary.md
├── examples/
│   ├── markdown/
│   │   ├── intro.md
│   │   ├── getting_started.md
│   │   └── advanced_usage.md
│   ├── styles/
│   │   └── custom.css
│   ├── example_job.yaml
│   └── example_job.json
└── README.md
```

## Dependencies

- **Markdown Processing**: `markdown`
- **HTML to PDF**: `weasyprint`
- **PDF Manipulation**: `PyPDF2`
- **HTML to Markdown**: `html2text`
- **Configuration**: `pyyaml` and `json`
- **OpenDocument Format**: `odfpy`
- **Image Processing**: `Pillow`

## Examples

The `examples` directory contains sample files to help you get started:

- Example Markdown files in `examples/markdown/`
- A custom CSS file in `examples/styles/`
- Example job files in both YAML and JSON formats

You can run the example with:

```bash
python src/doctool.py --job-file ./examples/example_job.yaml
```

## Development

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone git@github.com:Monotoba/doctool.git
   cd doctool
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please make sure your code follows the project's style guidelines and includes appropriate tests.

## Author

Developed by Randall Morgan ([@Monotoba](https://github.com/Monotoba))

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.