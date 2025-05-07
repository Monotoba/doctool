#!/usr/bin/env python3
"""
Markdown to HTML converter module.
Converts Markdown files to HTML.
"""

import os
import markdown
from typing import Dict, Any, List, Optional, Union


class MarkdownToHtmlConverter:
    """
    Converter for Markdown to HTML.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the converter.
        
        Args:
            options: Optional conversion options
        """
        self.options = options or {}
        
        # Default HTML template
        self.html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
{content}
</body>
</html>
"""
        
        # Default CSS
        self.default_css = """
body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }
code { font-family: monospace; }
h1, h2, h3 { color: #333; }
a { color: #0066cc; }
img { max-width: 100%; height: auto; }
"""
    
    def convert_file(self, input_file: str, output_file: str) -> str:
        """
        Convert a Markdown file to HTML.
        
        Args:
            input_file: Path to the input Markdown file
            output_file: Path to the output HTML file
            
        Returns:
            Path to the output HTML file
            
        Raises:
            FileNotFoundError: If the input file does not exist
            IOError: If there is an error reading or writing files
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        try:
            # Read markdown content
            with open(input_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Convert to HTML
            html_content = self.convert_text(md_content)
            
            # Get title from the first heading or use filename
            title = os.path.splitext(os.path.basename(input_file))[0].replace('_', ' ').title()
            if md_content.startswith('# '):
                title = md_content.split('\n')[0].lstrip('# ')
            
            # Get CSS
            css = self.default_css
            if 'css' in self.options and os.path.exists(self.options['css']):
                with open(self.options['css'], 'r', encoding='utf-8') as f:
                    css = f.read()
            
            # Insert into template
            full_html = self.html_template.format(title=title, content=html_content, css=css)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Write HTML file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            return output_file
        except Exception as e:
            raise IOError(f"Error converting {input_file} to HTML: {e}")
    
    def convert_text(self, md_text: str) -> str:
        """
        Convert Markdown text to HTML.
        
        Args:
            md_text: Markdown text to convert
            
        Returns:
            HTML content
        """
        # Convert to HTML with extensions
        extensions = self.options.get('markdown_extensions', [])
        
        # Add default extensions if none specified
        if not extensions:
            extensions = ['tables', 'fenced_code', 'codehilite']
        
        return markdown.markdown(md_text, extensions=extensions)
    
    def convert_directory(self, input_dir: str, output_dir: str, file_pattern: str = '*.md') -> List[str]:
        """
        Convert all Markdown files in a directory to HTML.
        
        Args:
            input_dir: Path to the input directory
            output_dir: Path to the output directory
            file_pattern: Pattern to match Markdown files (default: *.md)
            
        Returns:
            List of output HTML file paths
            
        Raises:
            FileNotFoundError: If the input directory does not exist
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all markdown files
        import glob
        md_files = glob.glob(os.path.join(input_dir, file_pattern))
        
        output_files = []
        for md_file in md_files:
            # Get the filename without extension
            base_name = os.path.basename(md_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            html_file = os.path.join(output_dir, file_name_without_ext + '.html')
            
            try:
                output_file = self.convert_file(md_file, html_file)
                output_files.append(output_file)
                print(f"Successfully converted {md_file} to {html_file}")
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
                import traceback
                traceback.print_exc()
        
        return output_files


def convert_md_to_html(input_path: str, output_path: str, options: Optional[Dict[str, Any]] = None) -> Union[str, List[str]]:
    """
    Convert Markdown to HTML.
    
    Args:
        input_path: Path to the input Markdown file or directory
        output_path: Path to the output HTML file or directory
        options: Optional conversion options
        
    Returns:
        Path to the output HTML file or list of output HTML file paths
        
    Raises:
        FileNotFoundError: If the input file or directory does not exist
    """
    converter = MarkdownToHtmlConverter(options)
    
    if os.path.isdir(input_path):
        return converter.convert_directory(input_path, output_path)
    else:
        return converter.convert_file(input_path, output_path)