#!/usr/bin/env python3
"""
Core converter module for document conversion tool.
Handles orchestration of the conversion process.
"""

import os
import glob
from typing import Dict, Any, List, Optional, Union, Tuple

from ..job.job_parser import JobParser, find_job_file, load_job_file


class ConversionManager:
    """
    Manager for document conversion processes.
    Orchestrates the conversion of documents based on job data.
    """
    
    def __init__(self, job_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the conversion manager.
        
        Args:
            job_data: Optional job data to use for conversion
        """
        self.job_data = job_data
        self.input_files = []
        self.output_files = []
    
    def load_job_file(self, file_path: str) -> None:
        """
        Load a job file and set it as the current job.
        
        Args:
            file_path: Path to the job file
        """
        self.job_data = load_job_file(file_path)
    
    def auto_detect_job_file(self) -> bool:
        """
        Auto-detect a job file in the current directory.
        
        Returns:
            True if a job file was found and loaded, False otherwise
        """
        job_file = find_job_file()
        if job_file:
            self.load_job_file(job_file)
            return True
        return False
    
    def set_job_data(self, job_data: Dict[str, Any]) -> None:
        """
        Set the job data directly.
        
        Args:
            job_data: Job data to use for conversion
        """
        self.job_data = job_data
    
    def prepare_conversion(self) -> None:
        """
        Prepare for conversion by gathering input files and creating output directories.
        
        Raises:
            ValueError: If job data is not set or invalid
        """
        if not self.job_data:
            raise ValueError("Job data not set. Load a job file or set job data directly.")
        
        # Get input files
        self._gather_input_files()
        
        # Create output directories
        self._prepare_output_directories()
    
    def _gather_input_files(self) -> None:
        """Gather input files based on job data."""
        input_data = self.job_data['input']
        input_format = input_data['format'].lower()
        
        # Normalize format
        if input_format == 'md':
            input_format = 'markdown'
        
        # Get file extension for the input format
        ext_map = {
            'markdown': '.md',
            'html': '.html',
            'pdf': '.pdf',
            'odt': '.odt'
        }
        file_ext = ext_map.get(input_format, '.md')
        
        # Gather files from directory or use specified files
        if 'directory' in input_data:
            input_dir = input_data['directory']
            if not os.path.exists(input_dir):
                raise ValueError(f"Input directory does not exist: {input_dir}")
            
            # Get all files with the specified extension
            self.input_files = glob.glob(os.path.join(input_dir, f'*{file_ext}'))
            
            # If documents section is present, filter and order files accordingly
            if 'documents' in self.job_data:
                ordered_files = []
                for doc in self.job_data['documents']:
                    file_path = os.path.join(input_dir, doc['file'])
                    if os.path.exists(file_path):
                        ordered_files.append((file_path, doc.get('title', None)))
                    else:
                        print(f"Warning: Document file not found: {file_path}")
                
                # Replace input_files with ordered files
                self.input_files = [f[0] for f in ordered_files]
        
        elif 'files' in input_data:
            # Use specified files
            self.input_files = []
            for file_path in input_data['files']:
                if os.path.exists(file_path):
                    self.input_files.append(file_path)
                else:
                    print(f"Warning: Input file not found: {file_path}")
        
        print(f"Found {len(self.input_files)} input files")
    
    def _prepare_output_directories(self) -> None:
        """Create output directories based on job data."""
        output_data = self.job_data['output']
        
        if 'directory' in output_data:
            output_dir = output_data['directory']
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created output directory: {output_dir}")
    
    def run_conversion(self) -> List[str]:
        """
        Run the conversion process based on job data.
        
        Returns:
            List of output file paths
        
        Raises:
            ValueError: If job data is not set or invalid
        """
        if not self.job_data:
            raise ValueError("Job data not set. Load a job file or set job data directly.")
        
        if not self.input_files:
            self.prepare_conversion()
        
        input_format = self.job_data['input']['format'].lower()
        output_format = self.job_data['output']['format'].lower()
        
        # Normalize formats
        if input_format == 'md':
            input_format = 'markdown'
        if output_format == 'md':
            output_format = 'markdown'
        
        # Skip conversion if input and output formats are the same
        if input_format == output_format:
            print(f"Input and output formats are the same ({input_format}). Copying files...")
            self._copy_files()
            return self.output_files
        
        # Determine conversion path
        conversion_path = self._determine_conversion_path(input_format, output_format)
        print(f"Conversion path: {' -> '.join(conversion_path)}")
        
        # Perform conversion
        self._convert_files(conversion_path)
        
        # Combine files if requested
        if 'combine' in self.job_data and self.job_data['combine'].get('enabled', False):
            self._combine_files()
        
        return self.output_files
    
    def _determine_conversion_path(self, input_format: str, output_format: str) -> List[str]:
        """
        Determine the conversion path from input format to output format.
        
        Args:
            input_format: Input format (markdown, html, pdf, odt)
            output_format: Output format (markdown, html, pdf, odt)
            
        Returns:
            List of formats representing the conversion path
            
        Raises:
            ValueError: If no conversion path is available
        """
        # Direct conversion paths
        direct_paths = {
            ('markdown', 'html'): ['markdown', 'html'],
            ('markdown', 'pdf'): ['markdown', 'html', 'pdf'],
            ('markdown', 'odt'): ['markdown', 'odt'],
            ('html', 'markdown'): ['html', 'markdown'],
            ('html', 'pdf'): ['html', 'pdf'],
            ('html', 'odt'): ['html', 'odt'],
            ('pdf', 'html'): ['pdf', 'html'],
            ('pdf', 'markdown'): ['pdf', 'html', 'markdown'],
            ('pdf', 'odt'): ['pdf', 'odt'],
            ('odt', 'html'): ['odt', 'html'],
            ('odt', 'markdown'): ['odt', 'html', 'markdown'],
            ('odt', 'pdf'): ['odt', 'pdf']
        }
        
        path = direct_paths.get((input_format, output_format))
        if not path:
            raise ValueError(f"No conversion path available from {input_format} to {output_format}")
        
        return path
    
    def _convert_files(self, conversion_path: List[str]) -> None:
        """
        Convert files along the specified conversion path.
        
        Args:
            conversion_path: List of formats representing the conversion path
        """
        # This is a placeholder for the actual conversion logic
        # In the real implementation, this would use the appropriate converter modules
        print(f"Converting files: {conversion_path}")
        
        # For now, just set output files to input files
        # This will be replaced with actual conversion logic
        self.output_files = self.input_files
    
    def _copy_files(self) -> None:
        """Copy files when input and output formats are the same."""
        # This is a placeholder for the actual copy logic
        # In the real implementation, this would copy files to the output directory
        print("Copying files")
        
        # For now, just set output files to input files
        # This will be replaced with actual copy logic
        self.output_files = self.input_files
    
    def _combine_files(self) -> None:
        """Combine output files into a single file if requested."""
        # This is a placeholder for the actual combine logic
        # In the real implementation, this would use the appropriate combiner module
        print("Combining files")
        
        # For now, just print a message
        # This will be replaced with actual combine logic
        combine_data = self.job_data['combine']
        output_file = combine_data['output_file']
        print(f"Combined output file: {output_file}")


def convert_documents(job_file: Optional[str] = None, job_data: Optional[Dict[str, Any]] = None) -> List[str]:
    """
    Convert documents based on a job file or job data.
    
    Args:
        job_file: Path to the job file (optional)
        job_data: Job data to use for conversion (optional)
        
    Returns:
        List of output file paths
        
    Raises:
        ValueError: If neither job_file nor job_data is provided
    """
    manager = ConversionManager()
    
    if job_file:
        manager.load_job_file(job_file)
    elif job_data:
        manager.set_job_data(job_data)
    else:
        # Try to auto-detect a job file
        if not manager.auto_detect_job_file():
            raise ValueError("No job file or job data provided")
    
    return manager.run_conversion()