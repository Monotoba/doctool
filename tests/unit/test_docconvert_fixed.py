"""
Unit tests for the main docconvert script.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Import directly from the doctool.py file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.doctool import parse_args, create_job_data_from_args, validate_args, main


@pytest.mark.unit
class TestDocconvert:
    """Tests for the main docconvert script."""
    
    def test_parse_args(self):
        """Test parsing command-line arguments."""
        # Test with no arguments
        with patch('sys.argv', ['docconvert.py']):
            args = parse_args()
            assert args.job_file is None
            assert args.input_dir is None
            assert args.input_file is None
            assert args.from_format is None
            assert args.output_dir is None
            assert args.output_file is None
            assert args.to_format is None
            assert args.combine is False
            assert args.files is None
            assert args.css is None
            assert args.toc is False
            assert args.embed_images is False
        
        # Test with job file
        with patch('sys.argv', ['docconvert.py', '--job-file', 'job.yaml']):
            args = parse_args()
            assert args.job_file == 'job.yaml'
        
        # Test with input and output options
        with patch('sys.argv', [
            'docconvert.py',
            '--input-dir', 'input',
            '--output-dir', 'output',
            '--from', 'md',
            '--to', 'html'
        ]):
            args = parse_args()
            assert args.input_dir == 'input'
            assert args.output_dir == 'output'
            assert args.from_format == 'md'
            assert args.to_format == 'html'
        
        # Test with combine options
        with patch('sys.argv', [
            'docconvert.py',
            '--combine',
            '--input-dir', 'input',
            '--output-file', 'combined.pdf',
            '--from', 'pdf',
            '--to', 'pdf',
            '--files', 'file1.pdf', 'file2.pdf'
        ]):
            args = parse_args()
            assert args.combine is True
            assert args.input_dir == 'input'
            assert args.output_file == 'combined.pdf'
            assert args.from_format == 'pdf'
            assert args.to_format == 'pdf'
            assert args.files == ['file1.pdf', 'file2.pdf']
    
    def test_create_job_data_from_args(self):
        """Test creating job data from command-line arguments."""
        # Test with input and output options
        args = MagicMock()
        args.input_dir = 'input'
        args.input_file = None
        args.from_format = 'md'
        args.output_dir = 'output'
        args.output_file = None
        args.to_format = 'html'
        args.css = None
        args.toc = False
        args.embed_images = False
        args.combine = False
        args.files = None
        
        job_data = create_job_data_from_args(args)
        
        assert job_data['input']['directory'] == 'input'
        assert job_data['input']['format'] == 'md'
        assert job_data['output']['directory'] == 'output'
        assert job_data['output']['format'] == 'html'
        assert 'css' not in job_data['options']
        assert 'toc' not in job_data['options']
        assert 'images' not in job_data['options']
        assert 'combine' not in job_data
        
        # Test with input file and output file
        args = MagicMock()
        args.input_dir = None
        args.input_file = 'input.md'
        args.from_format = 'md'
        args.output_dir = None
        args.output_file = 'output.html'
        args.to_format = 'html'
        args.css = 'style.css'
        args.toc = True
        args.embed_images = True
        args.combine = False
        args.files = None
        
        job_data = create_job_data_from_args(args)
        
        assert job_data['input']['files'] == ['input.md']
        assert job_data['input']['format'] == 'md'
        assert job_data['output']['file'] == 'output.html'
        assert job_data['output']['format'] == 'html'
        assert job_data['options']['css'] == 'style.css'
        assert job_data['options']['toc'] is True
        assert job_data['options']['images']['embed'] is True
        assert 'combine' not in job_data
        
        # Test with combine options
        args = MagicMock()
        args.input_dir = 'input'
        args.input_file = None
        args.from_format = 'pdf'
        args.output_dir = None
        args.output_file = 'combined.pdf'
        args.to_format = 'pdf'
        args.css = None
        args.toc = False
        args.embed_images = False
        args.combine = True
        args.files = ['file1.pdf', 'file2.pdf']
        
        job_data = create_job_data_from_args(args)
        
        assert job_data['input']['directory'] == 'input'
        assert job_data['input']['format'] == 'pdf'
        assert job_data['output']['file'] == 'combined.pdf'
        assert job_data['output']['format'] == 'pdf'
        assert job_data['combine']['enabled'] is True
        assert job_data['combine']['output_file'] == 'combined.pdf'
        assert len(job_data['documents']) == 2
        assert job_data['documents'][0]['file'] == 'file1.pdf'
        assert job_data['documents'][1]['file'] == 'file2.pdf'
    
    def test_validate_args(self):
        """Test validating command-line arguments."""
        # Test with job file
        args = MagicMock()
        args.job_file = 'job.yaml'
        
        assert validate_args(args) is True
        
        # Test with valid arguments
        args = MagicMock()
        args.job_file = None
        args.input_dir = 'input'
        args.input_file = None
        args.from_format = 'md'
        args.output_dir = 'output'
        args.output_file = None
        args.to_format = 'html'
        
        assert validate_args(args) is True
        
        # Test with missing input
        args = MagicMock()
        args.job_file = None
        args.input_dir = None
        args.input_file = None
        args.from_format = 'md'
        args.output_dir = 'output'
        args.output_file = None
        args.to_format = 'html'
        
        assert validate_args(args) is False
        
        # Test with missing output
        args = MagicMock()
        args.job_file = None
        args.input_dir = 'input'
        args.input_file = None
        args.from_format = 'md'
        args.output_dir = None
        args.output_file = None
        args.to_format = 'html'
        
        assert validate_args(args) is False
        
        # Test with missing format
        args = MagicMock()
        args.job_file = None
        args.input_dir = 'input'
        args.input_file = None
        args.from_format = None
        args.output_dir = 'output'
        args.output_file = None
        args.to_format = 'html'
        
        assert validate_args(args) is False
    
    @patch('src.doctool.convert_documents')
    @patch('src.doctool.find_job_file')
    @patch('src.doctool.validate_args')
    @patch('src.doctool.create_job_data_from_args')
    @patch('src.doctool.parse_args')
    def test_main(self, mock_parse_args, mock_create_job_data, mock_validate_args, mock_find_job_file, mock_convert_documents):
        """Test the main function."""
        # Test with job file
        mock_args = MagicMock()
        mock_args.job_file = 'job.yaml'
        mock_parse_args.return_value = mock_args
        mock_convert_documents.return_value = ['output.html']
        
        result = main()
        
        assert result == 0
        mock_parse_args.assert_called_once()
        mock_convert_documents.assert_called_once_with(job_file='job.yaml')
        
        # Reset mocks
        mock_parse_args.reset_mock()
        mock_convert_documents.reset_mock()
        
        # Test with command-line arguments
        mock_args = MagicMock()
        mock_args.job_file = None
        mock_parse_args.return_value = mock_args
        mock_validate_args.return_value = True
        mock_create_job_data.return_value = {'test': 'data'}
        mock_convert_documents.return_value = ['output.html']
        
        result = main()
        
        assert result == 0
        mock_parse_args.assert_called_once()
        mock_validate_args.assert_called_once_with(mock_args)
        mock_create_job_data.assert_called_once_with(mock_args)
        mock_convert_documents.assert_called_once_with(job_data={'test': 'data'})
        
        # Reset mocks
        mock_parse_args.reset_mock()
        mock_validate_args.reset_mock()
        mock_create_job_data.reset_mock()
        mock_convert_documents.reset_mock()
        
        # Test with auto-detected job file
        mock_args = MagicMock()
        mock_args.job_file = None
        mock_parse_args.return_value = mock_args
        mock_validate_args.return_value = False
        mock_find_job_file.return_value = 'auto_job.yaml'
        mock_convert_documents.return_value = ['output.html']
        
        result = main()
        
        assert result == 0
        mock_parse_args.assert_called_once()
        mock_validate_args.assert_called_once_with(mock_args)
        mock_find_job_file.assert_called_once()
        mock_convert_documents.assert_called_once_with(job_file='auto_job.yaml')
        
        # Reset mocks
        mock_parse_args.reset_mock()
        mock_validate_args.reset_mock()
        mock_find_job_file.reset_mock()
        mock_convert_documents.reset_mock()
        
        # Test with no job file found
        mock_args = MagicMock()
        mock_args.job_file = None
        mock_parse_args.return_value = mock_args
        mock_validate_args.return_value = False
        mock_find_job_file.return_value = None
        
        result = main()
        
        assert result == 1
        mock_parse_args.assert_called_once()
        mock_validate_args.assert_called_once_with(mock_args)
        mock_find_job_file.assert_called_once()
        mock_convert_documents.assert_not_called()
        
        # Reset mocks
        mock_parse_args.reset_mock()
        mock_validate_args.reset_mock()
        mock_find_job_file.reset_mock()
        mock_convert_documents.reset_mock()
        
        # Test with exception
        mock_args = MagicMock()
        mock_args.job_file = 'job.yaml'
        mock_parse_args.return_value = mock_args
        mock_convert_documents.side_effect = Exception("Test error")
        
        result = main()
        
        assert result == 1
        mock_parse_args.assert_called_once()
        mock_convert_documents.assert_called_once_with(job_file='job.yaml')