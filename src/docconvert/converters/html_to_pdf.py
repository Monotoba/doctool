#!/usr/bin/env python3
"""
HTML to PDF converter module.
Converts HTML files to PDF using WeasyPrint.
"""

import os
import glob
from weasyprint import HTML, CSS
from typing import Dict, Any, List, Optional, Union


class HtmlToPdfConverter:
    """
    Converter for HTML to PDF.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the converter.
        
        Args:
            options: Optional conversion options
        """
        self.options = options or {}
    
    def convert_file(self, input_file: str, output_file: str) -> str:
        """
        Convert an HTML file to PDF.
        
        Args:
            input_file: Path to the input HTML file
            output_file: Path to the output PDF file
            
        Returns:
            Path to the output PDF file
            
        Raises:
            FileNotFoundError: If the input file does not exist
            IOError: If there is an error reading or writing files
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Create HTML object
            html = HTML(filename=input_file)
            
            # Apply custom CSS if provided
            stylesheets = []
            if 'css' in self.options and os.path.exists(self.options['css']):
                stylesheets.append(CSS(filename=self.options['css']))
            
            # Convert HTML to PDF
            html.write_pdf(output_file, stylesheets=stylesheets)
            
            return output_file
        except Exception as e:
            raise IOError(f"Error converting {input_file} to PDF: {e}")
    
    def convert_directory(self, input_dir: str, output_dir: str, file_pattern: str = '*.html') -> List[str]:
        """
        Convert all HTML files in a directory to PDF.
        
        Args:
            input_dir: Path to the input directory
            output_dir: Path to the output directory
            file_pattern: Pattern to match HTML files (default: *.html)
            
        Returns:
            List of output PDF file paths
            
        Raises:
            FileNotFoundError: If the input directory does not exist
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all HTML files
        html_files = glob.glob(os.path.join(input_dir, file_pattern))
        
        output_files = []
        for html_file in html_files:
            # Get the filename without extension
            base_name = os.path.basename(html_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            pdf_file = os.path.join(output_dir, file_name_without_ext + '.pdf')
            
            try:
                output_file = self.convert_file(html_file, pdf_file)
                output_files.append(output_file)
                print(f"Successfully converted {html_file} to {pdf_file}")
            except Exception as e:
                print(f"Error processing {html_file}: {e}")
                import traceback
                traceback.print_exc()
        
        return output_files


def convert_html_to_pdf(input_path: str, output_path: str, options: Optional[Dict[str, Any]] = None, file_pattern: str = '*.html') -> Union[str, List[str]]:
    """
    Convert HTML to PDF.
    
    Args:
        input_path: Path to the input HTML file or directory
        output_path: Path to the output PDF file or directory
        options: Optional conversion options
        file_pattern: Pattern to match HTML files when input_path is a directory (default: *.html)
        
    Returns:
        Path to the output PDF file or list of output PDF file paths
        
    Raises:
        FileNotFoundError: If the input file or directory does not exist
    """
    converter = HtmlToPdfConverter(options)
    
    if os.path.isdir(input_path):
        return converter.convert_directory(input_path, output_path, file_pattern=file_pattern)
    else:
        return converter.convert_file(input_path, output_path)