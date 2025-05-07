#!/usr/bin/env python3
"""
Test script to check if imports work.
"""

import os
import sys

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

try:
    from src.docconvert.job.job_parser import load_job_file
    print("Successfully imported load_job_file")
except ImportError as e:
    print("Error importing load_job_file:", e)

try:
    from src.docconvert.core.converter import convert_documents
    print("Successfully imported convert_documents")
except ImportError as e:
    print("Error importing convert_documents:", e)

print("Import test completed.")