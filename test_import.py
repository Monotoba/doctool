#!/usr/bin/env python3
"""
Test script to check imports.
"""

try:
    from src.docconvert.job.job_parser import load_job_file
    print("Successfully imported job_parser")
except ImportError as e:
    print(f"Error importing job_parser: {e}")

try:
    from src.docconvert.core.converter import convert_documents
    print("Successfully imported converter")
except ImportError as e:
    print(f"Error importing converter: {e}")