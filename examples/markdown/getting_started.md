# Getting Started

This section will guide you through the process of installing and using the Document Conversion Tool.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/document-conversion-tool.git
   cd document-conversion-tool
   ```

2. Install dependencies:
   ```bash
   pip install markdown weasyprint PyPDF2 pyyaml html2text odfpy Pillow
   ```

## Basic Usage

### Command-Line Interface

The Document Conversion Tool provides a simple command-line interface for basic conversions:

```bash
# Convert a Markdown file to HTML
python src/docconvert.py --input-file ./input.md --output-file ./output.html --from md --to html

# Convert a Markdown file to PDF
python src/docconvert.py --input-file ./input.md --output-file ./output.pdf --from md --to pdf

# Convert all Markdown files in a directory to HTML
python src/docconvert.py --input-dir ./docs --output-dir ./html --from md --to html
```

### Using Job Files

For more complex conversion tasks, you can use job files in YAML or JSON format:

```bash
# Use a YAML job file
python src/docconvert.py --job-file ./my_job.yaml

# Use a JSON job file
python src/docconvert.py --job-file ./my_job.json
```

If you run the tool without any arguments, it will look for a `.yaml` or `.json` file in the current directory and use that as the job file.

## Example Job File

Here's a simple example of a job file in YAML format:

```yaml
input:
  directory: ./docs
  format: markdown
  
output:
  directory: ./output
  format: pdf
  
options:
  css: ./styles/custom.css
  toc: true
  
documents:
  - title: "Introduction"
    file: intro.md
  - title: "Chapter 1"
    file: chapter1.md
  - title: "Chapter 2"
    file: chapter2.md
    
combine:
  enabled: true
  output_file: complete_manual.pdf
  metadata:
    title: "Complete Manual"
    author: "Documentation Team"
```

This job file will:
1. Convert all Markdown files in the `./docs` directory to PDF
2. Apply custom CSS from `./styles/custom.css`
3. Generate a table of contents
4. Combine the specified documents into a single PDF file
5. Add metadata to the combined PDF