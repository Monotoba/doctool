#!/usr/bin/env python3
"""
HTML to Markdown converter module.
Converts HTML files to Markdown.
"""

import os
import html2text
from typing import Dict, Any, List, Optional, Union


class HtmlToMarkdownConverter:
    """
    Converter for HTML to Markdown.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the converter.
        
        Args:
            options: Optional conversion options
        """
        self.options = options or {}
        
        # Configure html2text
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = self.options.get('ignore_links', False)
        self.h2t.ignore_images = self.options.get('ignore_images', False)
        self.h2t.ignore_tables = self.options.get('ignore_tables', False)
        self.h2t.body_width = self.options.get('body_width', 0)  # 0 means no wrapping
        self.h2t.protect_links = self.options.get('protect_links', True)
        self.h2t.unicode_snob = self.options.get('unicode_snob', True)
        self.h2t.images_to_alt = self.options.get('images_to_alt', False)
        self.h2t.default_image_alt = self.options.get('default_image_alt', '')
    
    def convert_file(self, input_file: str, output_file: str) -> str:
        """
        Convert an HTML file to Markdown.
        
        Args:
            input_file: Path to the input HTML file
            output_file: Path to the output Markdown file
            
        Returns:
            Path to the output Markdown file
            
        Raises:
            FileNotFoundError: If the input file does not exist
            IOError: If there is an error reading or writing files
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        try:
            # Read HTML content
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Convert to Markdown
            md_content = self.convert_text(html_content)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Write Markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return output_file
        except Exception as e:
            raise IOError(f"Error converting {input_file} to Markdown: {e}")
    
    def convert_text(self, html_text: str) -> str:
        """
        Convert HTML text to Markdown.
        
        Args:
            html_text: HTML text to convert
            
        Returns:
            Markdown content
        """
        return self.h2t.handle(html_text)
    
    def convert_directory(self, input_dir: str, output_dir: str, file_pattern: str = '*.html') -> List[str]:
        """
        Convert all HTML files in a directory to Markdown.
        
        Args:
            input_dir: Path to the input directory
            output_dir: Path to the output directory
            file_pattern: Pattern to match HTML files (default: *.html)
            
        Returns:
            List of output Markdown file paths
            
        Raises:
            FileNotFoundError: If the input directory does not exist
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all HTML files
        import glob
        html_files = glob.glob(os.path.join(input_dir, file_pattern))
        
        output_files = []
        for html_file in html_files:
            # Get the filename without extension
            base_name = os.path.basename(html_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            md_file = os.path.join(output_dir, file_name_without_ext + '.md')
            
            try:
                output_file = self.convert_file(html_file, md_file)
                output_files.append(output_file)
                print(f"Successfully converted {html_file} to {md_file}")
            except Exception as e:
                print(f"Error processing {html_file}: {e}")
                import traceback
                traceback.print_exc()
        
        return output_files


def convert_html_to_markdown(input_path: str, output_path: str, options: Optional[Dict[str, Any]] = None) -> Union[str, List[str]]:
    """
    Convert HTML to Markdown.
    
    Args:
        input_path: Path to the input HTML file or directory
        output_path: Path to the output Markdown file or directory
        options: Optional conversion options
        
    Returns:
        Path to the output Markdown file or list of output Markdown file paths
        
    Raises:
        FileNotFoundError: If the input file or directory does not exist
    """
    converter = HtmlToMarkdownConverter(options)
    
    if os.path.isdir(input_path):
        return converter.convert_directory(input_path, output_path)
    else:
        return converter.convert_file(input_path, output_path)