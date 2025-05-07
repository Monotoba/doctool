#!/usr/bin/env python3
"""
Job parser module for document conversion tool.
Handles parsing and validation of YAML and JSON job files.
"""

import os
import json
import yaml
from typing import Dict, Any, List, Optional, Union


class JobParser:
    """
    Parser for document conversion job files (YAML/JSON).
    """
    
    def __init__(self):
        """Initialize the job parser."""
        self.job_data = None
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a job file (YAML or JSON) and return the job data.
        
        Args:
            file_path: Path to the job file
            
        Returns:
            Dict containing the parsed job data
            
        Raises:
            FileNotFoundError: If the job file does not exist
            ValueError: If the job file format is not supported or invalid
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Job file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_ext == '.yaml' or file_ext == '.yml':
                    self.job_data = yaml.safe_load(f)
                elif file_ext == '.json':
                    self.job_data = json.load(f)
                else:
                    raise ValueError(f"Unsupported job file format: {file_ext}")
                
            # Validate the job data
            self._validate_job_data()
            
            return self.job_data
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def _validate_job_data(self) -> None:
        """
        Validate the job data structure.
        
        Raises:
            ValueError: If the job data is invalid
        """
        if not self.job_data:
            raise ValueError("Job data is empty")
        
        # Check for required sections
        required_sections = ['input', 'output']
        for section in required_sections:
            if section not in self.job_data:
                raise ValueError(f"Missing required section: {section}")
        
        # Validate input section
        self._validate_input_section()
        
        # Validate output section
        self._validate_output_section()
        
        # Validate options section if present
        if 'options' in self.job_data:
            self._validate_options_section()
        
        # Validate documents section if present
        if 'documents' in self.job_data:
            self._validate_documents_section()
        
        # Validate combine section if present
        if 'combine' in self.job_data:
            self._validate_combine_section()
    
    def _validate_input_section(self) -> None:
        """Validate the input section of the job data."""
        input_data = self.job_data['input']
        
        # Check for required fields
        if 'format' not in input_data:
            raise ValueError("Missing required field: input.format")
        
        # Either directory or files must be specified
        if 'directory' not in input_data and 'files' not in input_data:
            raise ValueError("Either input.directory or input.files must be specified")
        
        # Validate format
        valid_formats = ['markdown', 'md', 'html', 'pdf', 'odt']
        if input_data['format'].lower() not in valid_formats:
            raise ValueError(f"Invalid input format: {input_data['format']}. "
                            f"Must be one of: {', '.join(valid_formats)}")
    
    def _validate_output_section(self) -> None:
        """Validate the output section of the job data."""
        output_data = self.job_data['output']
        
        # Check for required fields
        if 'format' not in output_data:
            raise ValueError("Missing required field: output.format")
        
        # Either directory or file must be specified
        if 'directory' not in output_data and 'file' not in output_data:
            raise ValueError("Either output.directory or output.file must be specified")
        
        # Validate format
        valid_formats = ['markdown', 'md', 'html', 'pdf', 'odt']
        if output_data['format'].lower() not in valid_formats:
            raise ValueError(f"Invalid output format: {output_data['format']}. "
                            f"Must be one of: {', '.join(valid_formats)}")
    
    def _validate_options_section(self) -> None:
        """Validate the options section of the job data."""
        options_data = self.job_data['options']
        
        # Validate CSS file if specified
        if 'css' in options_data and not os.path.exists(options_data['css']):
            print(f"Warning: CSS file not found: {options_data['css']}")
        
        # Validate cover page if specified
        if 'cover_page' in options_data and not os.path.exists(options_data['cover_page']):
            print(f"Warning: Cover page file not found: {options_data['cover_page']}")
        
        # Validate images section if present
        if 'images' in options_data:
            self._validate_images_section(options_data['images'])
    
    def _validate_images_section(self, images_data: Dict[str, Any]) -> None:
        """Validate the images section of the options."""
        # Validate embed flag
        if 'embed' in images_data and not isinstance(images_data['embed'], bool):
            raise ValueError("options.images.embed must be a boolean")
        
        # Validate formats list
        if 'formats' in images_data:
            if not isinstance(images_data['formats'], list):
                raise ValueError("options.images.formats must be a list")
            
            valid_formats = ['jpg', 'jpeg', 'png', 'webp', 'svg']
            for fmt in images_data['formats']:
                if fmt.lower() not in valid_formats:
                    raise ValueError(f"Invalid image format: {fmt}. "
                                    f"Must be one of: {', '.join(valid_formats)}")
    
    def _validate_documents_section(self) -> None:
        """Validate the documents section of the job data."""
        documents_data = self.job_data['documents']
        
        if not isinstance(documents_data, list):
            raise ValueError("documents section must be a list")
        
        for i, doc in enumerate(documents_data):
            if not isinstance(doc, dict):
                raise ValueError(f"Document at index {i} must be an object")
            
            if 'file' not in doc:
                raise ValueError(f"Missing required field: documents[{i}].file")
            
            # Check if the file exists (relative to input directory if specified)
            if 'directory' in self.job_data['input']:
                file_path = os.path.join(self.job_data['input']['directory'], doc['file'])
                if not os.path.exists(file_path):
                    print(f"Warning: Document file not found: {file_path}")
    
    def _validate_combine_section(self) -> None:
        """Validate the combine section of the job data."""
        combine_data = self.job_data['combine']
        
        if not isinstance(combine_data, dict):
            raise ValueError("combine section must be an object")
        
        # Check for required fields
        if 'enabled' not in combine_data:
            raise ValueError("Missing required field: combine.enabled")
        
        if not isinstance(combine_data['enabled'], bool):
            raise ValueError("combine.enabled must be a boolean")
        
        if combine_data['enabled'] and 'output_file' not in combine_data:
            raise ValueError("Missing required field: combine.output_file when combine.enabled is true")


def find_job_file(directory: str = '.') -> Optional[str]:
    """
    Find a job file (YAML or JSON) in the specified directory.
    
    Args:
        directory: Directory to search for job files (default: current directory)
        
    Returns:
        Path to the job file if found, None otherwise
    """
    # Look for .yaml files first, then .json
    for ext in ['.yaml', '.yml', '.json']:
        for file in os.listdir(directory):
            if file.endswith(ext):
                return os.path.join(directory, file)
    
    return None


def load_job_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a job file.
    
    Args:
        file_path: Path to the job file
        
    Returns:
        Dict containing the parsed job data
    """
    parser = JobParser()
    return parser.parse_file(file_path)