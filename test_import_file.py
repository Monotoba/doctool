#!/usr/bin/env python3
"""
Test script to check imports and write results to a file.
"""

with open('import_test_results.txt', 'w') as f:
    try:
        from src.docconvert.job.job_parser import load_job_file
        f.write("Successfully imported job_parser\n")
    except ImportError as e:
        f.write(f"Error importing job_parser: {e}\n")

    try:
        from src.docconvert.core.converter import convert_documents
        f.write("Successfully imported converter\n")
    except ImportError as e:
        f.write(f"Error importing converter: {e}\n")