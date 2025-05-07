"""
Unit tests for the job parser module.
"""

import os
import pytest
from src.docconvert.job.job_parser import JobParser, find_job_file, load_job_file


@pytest.mark.unit
class TestJobParser:
    """Tests for the JobParser class."""
    
    def test_parse_yaml_file(self, sample_yaml_job):
        """Test parsing a YAML job file."""
        file_path, expected_data = sample_yaml_job
        
        parser = JobParser()
        job_data = parser.parse_file(file_path)
        
        assert job_data is not None
        assert job_data["input"]["format"] == expected_data["input"]["format"]
        assert job_data["output"]["format"] == expected_data["output"]["format"]
        assert job_data["options"]["toc"] == expected_data["options"]["toc"]
    
    def test_parse_json_file(self, sample_json_job):
        """Test parsing a JSON job file."""
        file_path, expected_data = sample_json_job
        
        parser = JobParser()
        job_data = parser.parse_file(file_path)
        
        assert job_data is not None
        assert job_data["input"]["format"] == expected_data["input"]["format"]
        assert job_data["output"]["format"] == expected_data["output"]["format"]
        assert job_data["options"]["toc"] == expected_data["options"]["toc"]
    
    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file."""
        parser = JobParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse_file("/nonexistent/file.yaml")
    
    def test_parse_invalid_format(self, temp_dir):
        """Test parsing a file with an invalid format."""
        file_path = os.path.join(temp_dir, "invalid.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("This is not a valid YAML or JSON file.")
        
        parser = JobParser()
        
        with pytest.raises(ValueError):
            parser.parse_file(file_path)
    
    def test_validate_job_data_missing_section(self, sample_yaml_job):
        """Test validation of job data with a missing required section."""
        file_path, _ = sample_yaml_job
        
        parser = JobParser()
        job_data = parser.parse_file(file_path)
        
        # Remove a required section
        del job_data["input"]
        parser.job_data = job_data
        
        with pytest.raises(ValueError):
            parser._validate_job_data()
    
    def test_validate_input_section_missing_format(self, sample_yaml_job):
        """Test validation of input section with missing format."""
        file_path, _ = sample_yaml_job
        
        parser = JobParser()
        job_data = parser.parse_file(file_path)
        
        # Remove format from input section
        del job_data["input"]["format"]
        parser.job_data = job_data
        
        with pytest.raises(ValueError):
            parser._validate_input_section()
    
    def test_validate_input_section_invalid_format(self, sample_yaml_job):
        """Test validation of input section with invalid format."""
        file_path, _ = sample_yaml_job
        
        parser = JobParser()
        job_data = parser.parse_file(file_path)
        
        # Set an invalid format
        job_data["input"]["format"] = "invalid"
        parser.job_data = job_data
        
        with pytest.raises(ValueError):
            parser._validate_input_section()


@pytest.mark.unit
class TestJobFileFunctions:
    """Tests for the job file utility functions."""
    
    def test_find_job_file(self, temp_dir, sample_yaml_job, sample_json_job):
        """Test finding a job file in a directory."""
        yaml_path, _ = sample_yaml_job
        json_path, _ = sample_json_job
        
        # Test finding YAML file first
        job_file = find_job_file(temp_dir)
        assert job_file is not None
        assert job_file.endswith(".yaml") or job_file.endswith(".yml") or job_file.endswith(".json")
    
    def test_find_job_file_nonexistent(self, temp_dir):
        """Test finding a job file in a directory with no job files."""
        # Create a new empty directory
        empty_dir = os.path.join(temp_dir, "empty")
        os.makedirs(empty_dir, exist_ok=True)
        
        job_file = find_job_file(empty_dir)
        assert job_file is None
    
    def test_load_job_file(self, sample_yaml_job):
        """Test loading a job file."""
        file_path, expected_data = sample_yaml_job
        
        job_data = load_job_file(file_path)
        
        assert job_data is not None
        assert job_data["input"]["format"] == expected_data["input"]["format"]
        assert job_data["output"]["format"] == expected_data["output"]["format"]
        assert job_data["options"]["toc"] == expected_data["options"]["toc"]