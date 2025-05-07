#!/usr/bin/env python3
"""
Document Conversion Tool

A flexible, general-purpose document conversion tool that can convert between
various document formats (Markdown, HTML, PDF, OpenDocument) and optionally
combine multiple documents into a single file.

Usage:
    python doctool.py [options]
    python doctool.py --job-file my_job.yaml
    python doctool.py --input-dir ./docs --output-dir ./output --from md --to pdf
"""

import os
import sys
import argparse
from typing import Dict, Any, List, Optional, Union

from src.docconvert.core.converter import ConversionManager, convert_documents
from src.docconvert.job.job_parser import find_job_file, load_job_file


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Document Conversion Tool',
        epilog='If no arguments are provided, the tool will look for a .yaml or .json job file in the current directory.'
    )
    
    # Job file
    parser.add_argument('--job-file', '-j', help='Path to the job file (YAML or JSON)')
    
    # Input options
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument('--input-dir', help='Input directory containing documents to convert')
    input_group.add_argument('--input-file', help='Input file to convert')
    input_group.add_argument('--from', dest='from_format', choices=['md', 'markdown', 'html', 'pdf', 'odt'],
                            help='Input format')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--output-dir', help='Output directory for converted documents')
    output_group.add_argument('--output-file', help='Output file for converted document')
    output_group.add_argument('--to', dest='to_format', choices=['md', 'markdown', 'html', 'pdf', 'odt'],
                             help='Output format')
    
    # Combine options
    combine_group = parser.add_argument_group('Combine Options')
    combine_group.add_argument('--combine', action='store_true', help='Combine multiple documents into a single file')
    combine_group.add_argument('--files', nargs='+', help='List of files to combine (in order)')
    
    # Additional options
    options_group = parser.add_argument_group('Additional Options')
    options_group.add_argument('--css', help='Path to custom CSS file for HTML/PDF output')
    options_group.add_argument('--toc', action='store_true', help='Generate table of contents')
    options_group.add_argument('--embed-images', action='store_true', help='Embed images in the output document')
    
    return parser.parse_args()


def create_job_data_from_args(args) -> Dict[str, Any]:
    """
    Create job data from command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Dict containing job data
    """
    job_data = {
        'input': {},
        'output': {},
        'options': {}
    }
    
    # Input section
    if args.input_dir:
        job_data['input']['directory'] = args.input_dir
    elif args.input_file:
        job_data['input']['files'] = [args.input_file]
    
    if args.from_format:
        job_data['input']['format'] = args.from_format
    
    # Output section
    if args.output_dir:
        job_data['output']['directory'] = args.output_dir
    elif args.output_file:
        job_data['output']['file'] = args.output_file
    
    if args.to_format:
        job_data['output']['format'] = args.to_format
    
    # Options section
    if args.css:
        job_data['options']['css'] = args.css
    
    if args.toc:
        job_data['options']['toc'] = True
    
    if args.embed_images:
        job_data['options']['images'] = {
            'embed': True,
            'formats': ['jpg', 'jpeg', 'png', 'webp', 'svg']
        }
    
    # Combine section
    if args.combine:
        job_data['combine'] = {
            'enabled': True
        }
        
        if args.output_file:
            job_data['combine']['output_file'] = args.output_file
        
        if args.files:
            job_data['documents'] = []
            for file in args.files:
                job_data['documents'].append({
                    'file': file
                })
    
    return job_data


def validate_args(args) -> bool:
    """
    Validate command-line arguments.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        True if arguments are valid, False otherwise
    """
    # If job file is specified, no need to validate other arguments
    if args.job_file:
        return True
    
    # Check if required arguments are provided
    if not (args.input_dir or args.input_file):
        return False
    
    if not (args.output_dir or args.output_file):
        return False
    
    if not (args.from_format and args.to_format):
        return False
    
    return True


def main():
    """Main entry point for the document conversion tool."""
    args = parse_args()
    
    try:
        # If job file is specified, use it
        if args.job_file:
            output_files = convert_documents(job_file=args.job_file)
            print(f"Conversion completed. Output files: {output_files}")
            return 0
        
        # If command-line arguments are provided, create job data from them
        if validate_args(args):
            job_data = create_job_data_from_args(args)
            output_files = convert_documents(job_data=job_data)
            print(f"Conversion completed. Output files: {output_files}")
            return 0
        
        # If no arguments are provided, try to find a job file in the current directory
        job_file = find_job_file()
        if job_file:
            print(f"Using job file: {job_file}")
            output_files = convert_documents(job_file=job_file)
            print(f"Conversion completed. Output files: {output_files}")
            return 0
        
        # If no job file is found, print usage and exit
        print("Error: No job file found and insufficient command-line arguments provided.")
        print("Please specify a job file or provide the required command-line arguments.")
        print("Run 'python doctool.py --help' for more information.")
        return 1
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
