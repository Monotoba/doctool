#!/usr/bin/env python3
"""
PDF combiner module.
Combines multiple PDF files into a single PDF.
"""

import os
import glob
from PyPDF2 import PdfMerger
from typing import Dict, Any, List, Optional, Union


class PdfCombiner:
    """
    Combiner for PDF files.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the combiner.
        
        Args:
            options: Optional combination options
        """
        self.options = options or {}
    
    def combine_files(self, input_files: List[str], output_file: str) -> str:
        """
        Combine multiple PDF files into a single PDF.
        
        Args:
            input_files: List of input PDF file paths
            output_file: Path to the output combined PDF file
            
        Returns:
            Path to the output combined PDF file
            
        Raises:
            FileNotFoundError: If any input file does not exist
            IOError: If there is an error reading or writing files
        """
        # Check if all input files exist
        for input_file in input_files:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file not found: {input_file}")
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            # Create a PDF merger object
            merger = PdfMerger()
            
            # Add metadata if provided
            if 'metadata' in self.options:
                metadata = self.options['metadata']
                if 'title' in metadata:
                    merger.add_metadata({'/Title': metadata['title']})
                if 'author' in metadata:
                    merger.add_metadata({'/Author': metadata['author']})
                if 'subject' in metadata:
                    merger.add_metadata({'/Subject': metadata['subject']})
                if 'keywords' in metadata:
                    merger.add_metadata({'/Keywords': metadata['keywords']})
            
            # Add each PDF to the merger
            for input_file in input_files:
                print(f"Adding {input_file} to the combined PDF")
                try:
                    merger.append(input_file)
                except Exception as e:
                    print(f"Error adding {input_file}: {e}")
                    raise
            
            # Write the combined PDF to disk
            print(f"Writing combined PDF to {output_file}")
            merger.write(output_file)
            merger.close()
            
            return output_file
        except Exception as e:
            raise IOError(f"Error combining PDF files: {e}")
    
    def combine_directory(self, input_dir: str, output_file: str, file_pattern: str = '*.pdf', file_order: Optional[List[str]] = None) -> str:
        """
        Combine all PDF files in a directory into a single PDF.
        
        Args:
            input_dir: Path to the input directory
            output_file: Path to the output combined PDF file
            file_pattern: Pattern to match PDF files (default: *.pdf)
            file_order: Optional list of filenames to specify the order
            
        Returns:
            Path to the output combined PDF file
            
        Raises:
            FileNotFoundError: If the input directory does not exist
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Get all PDF files
        pdf_files = glob.glob(os.path.join(input_dir, file_pattern))
        
        # Sort files by name if no order is specified
        if not file_order:
            pdf_files.sort()
        else:
            # Order files according to the specified order
            ordered_files = []
            for filename in file_order:
                file_path = os.path.join(input_dir, filename)
                if os.path.exists(file_path):
                    ordered_files.append(file_path)
                else:
                    print(f"Warning: Ordered file not found: {file_path}")
            
            # Add any remaining files that weren't in the order list
            for file_path in pdf_files:
                if file_path not in ordered_files:
                    ordered_files.append(file_path)
            
            pdf_files = ordered_files
        
        return self.combine_files(pdf_files, output_file)


def combine_pdfs(input_paths: Union[str, List[str]], output_path: str, options: Optional[Dict[str, Any]] = None, file_pattern: str = '*.pdf') -> str:
    """
    Combine PDF files into a single PDF.
    
    Args:
        input_paths: Path to the input directory or list of input PDF file paths
        output_path: Path to the output combined PDF file
        options: Optional combination options
        file_pattern: Pattern to match PDF files when input_paths is a directory (default: *.pdf)
        
    Returns:
        Path to the output combined PDF file
        
    Raises:
        FileNotFoundError: If the input directory or any input file does not exist
    """
    combiner = PdfCombiner(options)
    
    if isinstance(input_paths, str) and os.path.isdir(input_paths):
        file_order = options.get('file_order') if options else None
        return combiner.combine_directory(input_paths, output_path, file_pattern=file_pattern, file_order=file_order)
    elif isinstance(input_paths, list):
        return combiner.combine_files(input_paths, output_path)
    else:
        raise ValueError("input_paths must be a directory path or a list of file paths")