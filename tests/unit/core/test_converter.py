"""
Unit tests for the core converter module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.docconvert.core.converter import ConversionManager, convert_documents


@pytest.mark.unit
class TestConversionManager:
    """Tests for the ConversionManager class."""
    
    def test_init(self):
        """Test initialization of ConversionManager."""
        manager = ConversionManager()
        assert manager.job_data is None
        assert manager.input_files == []
        assert manager.output_files == []
        
        job_data = {"test": "data"}
        manager = ConversionManager(job_data)
        assert manager.job_data == job_data
    
    def test_load_job_file(self, sample_yaml_job):
        """Test loading a job file."""
        file_path, expected_data = sample_yaml_job
        
        manager = ConversionManager()
        manager.load_job_file(file_path)
        
        assert manager.job_data is not None
        assert manager.job_data["input"]["format"] == expected_data["input"]["format"]
        assert manager.job_data["output"]["format"] == expected_data["output"]["format"]
    
    @patch('src.docconvert.core.converter.find_job_file')
    @patch('src.docconvert.core.converter.load_job_file')
    def test_auto_detect_job_file(self, mock_load_job_file, mock_find_job_file, sample_yaml_job):
        """Test auto-detecting a job file."""
        file_path, expected_data = sample_yaml_job
        mock_find_job_file.return_value = file_path
        mock_load_job_file.return_value = expected_data
        
        manager = ConversionManager()
        result = manager.auto_detect_job_file()
        
        assert result is True
        assert manager.job_data == expected_data
        mock_find_job_file.assert_called_once()
        mock_load_job_file.assert_called_once_with(file_path)
    
    @patch('src.docconvert.core.converter.find_job_file')
    def test_auto_detect_job_file_not_found(self, mock_find_job_file):
        """Test auto-detecting a job file when none exists."""
        mock_find_job_file.return_value = None
        
        manager = ConversionManager()
        result = manager.auto_detect_job_file()
        
        assert result is False
        assert manager.job_data is None
        mock_find_job_file.assert_called_once()
    
    def test_set_job_data(self):
        """Test setting job data directly."""
        job_data = {"test": "data"}
        
        manager = ConversionManager()
        manager.set_job_data(job_data)
        
        assert manager.job_data == job_data
    
    def test_prepare_conversion_no_job_data(self):
        """Test preparing conversion with no job data."""
        manager = ConversionManager()
        
        with pytest.raises(ValueError):
            manager.prepare_conversion()
    
    @patch('os.path.exists')
    @patch('glob.glob')
    def test_gather_input_files_directory(self, mock_glob, mock_exists, temp_dir):
        """Test gathering input files from a directory."""
        mock_exists.return_value = True
        mock_glob.return_value = [
            os.path.join(temp_dir, "file1.md"),
            os.path.join(temp_dir, "file2.md")
        ]
        
        job_data = {
            "input": {
                "directory": temp_dir,
                "format": "markdown"
            },
            "output": {
                "directory": os.path.join(temp_dir, "output"),
                "format": "html"
            }
        }
        
        manager = ConversionManager(job_data)
        manager._gather_input_files()
        
        assert len(manager.input_files) == 2
        mock_exists.assert_called_once_with(temp_dir)
        mock_glob.assert_called_once()
    
    @patch('os.path.exists')
    def test_gather_input_files_files(self, mock_exists):
        """Test gathering input files from a list of files."""
        mock_exists.return_value = True
        
        files = ["/path/to/file1.md", "/path/to/file2.md"]
        job_data = {
            "input": {
                "files": files,
                "format": "markdown"
            },
            "output": {
                "directory": "/path/to/output",
                "format": "html"
            }
        }
        
        manager = ConversionManager(job_data)
        manager._gather_input_files()
        
        assert manager.input_files == files
        assert mock_exists.call_count == 2
    
    @patch('os.makedirs')
    def test_prepare_output_directories(self, mock_makedirs, temp_dir):
        """Test preparing output directories."""
        output_dir = os.path.join(temp_dir, "output")
        job_data = {
            "input": {
                "directory": temp_dir,
                "format": "markdown"
            },
            "output": {
                "directory": output_dir,
                "format": "html"
            }
        }
        
        manager = ConversionManager(job_data)
        manager._prepare_output_directories()
        
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
    
    def test_determine_conversion_path(self):
        """Test determining the conversion path."""
        manager = ConversionManager()
        
        # Test direct paths
        path = manager._determine_conversion_path("markdown", "html")
        assert path == ["markdown", "html"]
        
        path = manager._determine_conversion_path("markdown", "pdf")
        assert path == ["markdown", "html", "pdf"]
        
        path = manager._determine_conversion_path("html", "markdown")
        assert path == ["html", "markdown"]
        
        # Test invalid path
        with pytest.raises(ValueError):
            manager._determine_conversion_path("invalid", "format")


@pytest.mark.unit
class TestConvertDocuments:
    """Tests for the convert_documents function."""
    
    @patch('src.docconvert.core.converter.ConversionManager')
    def test_convert_documents_with_job_file(self, mock_manager_class, sample_yaml_job):
        """Test converting documents with a job file."""
        file_path, _ = sample_yaml_job
        
        mock_manager = MagicMock()
        mock_manager.run_conversion.return_value = ["output1.html", "output2.html"]
        mock_manager_class.return_value = mock_manager
        
        output_files = convert_documents(job_file=file_path)
        
        assert output_files == ["output1.html", "output2.html"]
        mock_manager.load_job_file.assert_called_once_with(file_path)
        mock_manager.run_conversion.assert_called_once()
    
    @patch('src.docconvert.core.converter.ConversionManager')
    def test_convert_documents_with_job_data(self, mock_manager_class):
        """Test converting documents with job data."""
        job_data = {"test": "data"}
        
        mock_manager = MagicMock()
        mock_manager.run_conversion.return_value = ["output1.html", "output2.html"]
        mock_manager_class.return_value = mock_manager
        
        output_files = convert_documents(job_data=job_data)
        
        assert output_files == ["output1.html", "output2.html"]
        mock_manager.set_job_data.assert_called_once_with(job_data)
        mock_manager.run_conversion.assert_called_once()
    
    @patch('src.docconvert.core.converter.ConversionManager')
    def test_convert_documents_auto_detect(self, mock_manager_class):
        """Test converting documents with auto-detection."""
        mock_manager = MagicMock()
        mock_manager.auto_detect_job_file.return_value = True
        mock_manager.run_conversion.return_value = ["output1.html", "output2.html"]
        mock_manager_class.return_value = mock_manager
        
        output_files = convert_documents()
        
        assert output_files == ["output1.html", "output2.html"]
        mock_manager.auto_detect_job_file.assert_called_once()
        mock_manager.run_conversion.assert_called_once()
    
    @patch('src.docconvert.core.converter.ConversionManager')
    def test_convert_documents_no_job(self, mock_manager_class):
        """Test converting documents with no job file or data."""
        mock_manager = MagicMock()
        mock_manager.auto_detect_job_file.return_value = False
        mock_manager_class.return_value = mock_manager
        
        with pytest.raises(ValueError):
            convert_documents()