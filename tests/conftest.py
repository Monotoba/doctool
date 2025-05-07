"""
Pytest configuration file for the document conversion tool tests.
"""

import os
import sys
import tempfile
import pytest
import yaml
import json

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def sample_yaml_job(temp_dir):
    """Create a sample YAML job file for tests."""
    job_data = {
        "input": {
            "directory": os.path.join(temp_dir, "input"),
            "format": "markdown"
        },
        "output": {
            "directory": os.path.join(temp_dir, "output"),
            "format": "html"
        },
        "options": {
            "css": os.path.join(temp_dir, "styles", "custom.css"),
            "toc": True,
            "images": {
                "embed": True,
                "formats": ["jpg", "png", "svg"]
            }
        }
    }
    
    # Create the job file
    file_path = os.path.join(temp_dir, "test_job.yaml")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(job_data, f)
    
    return file_path, job_data


@pytest.fixture
def sample_json_job(temp_dir):
    """Create a sample JSON job file for tests."""
    job_data = {
        "input": {
            "directory": os.path.join(temp_dir, "input"),
            "format": "markdown"
        },
        "output": {
            "directory": os.path.join(temp_dir, "output"),
            "format": "html"
        },
        "options": {
            "css": os.path.join(temp_dir, "styles", "custom.css"),
            "toc": True,
            "images": {
                "embed": True,
                "formats": ["jpg", "png", "svg"]
            }
        }
    }
    
    # Create the job file
    file_path = os.path.join(temp_dir, "test_job.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(job_data, f)
    
    return file_path, job_data


@pytest.fixture
def sample_md_file(temp_dir):
    """Create a sample Markdown file for tests."""
    # Create the directory
    input_dir = os.path.join(temp_dir, "input")
    os.makedirs(input_dir, exist_ok=True)
    
    # Create the Markdown file
    file_path = os.path.join(input_dir, "test.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("""# Test Document
        
This is a test document with some Markdown content.

## Section 1

- Item 1
- Item 2
- Item 3

## Section 2

Some more text here.
""")
    
    return file_path


@pytest.fixture
def sample_html_file(temp_dir):
    """Create a sample HTML file for tests."""
    # Create the directory
    input_dir = os.path.join(temp_dir, "input")
    os.makedirs(input_dir, exist_ok=True)
    
    # Create the HTML file
    file_path = os.path.join(input_dir, "test.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
</head>
<body>
    <h1>Test Document</h1>
    <p>This is a test document with some HTML content.</p>
    
    <h2>Section 1</h2>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
    
    <h2>Section 2</h2>
    <p>Some more text here.</p>
</body>
</html>
""")
    
    return file_path


@pytest.fixture
def sample_image_file(temp_dir):
    """Create a sample image file for tests."""
    # Create the directory
    input_dir = os.path.join(temp_dir, "input")
    os.makedirs(input_dir, exist_ok=True)
    
    # Create a simple image file (1x1 pixel black PNG)
    file_path = os.path.join(input_dir, "test.png")
    with open(file_path, 'wb') as f:
        # This is a minimal valid PNG file (1x1 pixel, black)
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\xe7Y\x00\x00\x00\x00IEND\xaeB`\x82')
    
    return file_path