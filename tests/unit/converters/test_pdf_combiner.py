"""
Unit tests for the PDF combiner module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.docconvert.converters.pdf_combiner import PdfCombiner, combine_pdfs


@pytest.mark.unit
class TestPdfCombiner:
    """Tests for the PdfCombiner class."""
    
    def test_init(self):
        """Test initialization of PdfCombiner."""
        combiner = PdfCombiner()
        assert combiner.options == {}
        
        options = {"test": "option"}
        combiner = PdfCombiner(options)
        assert combiner.options == options
    
    @patch('src.docconvert.converters.pdf_combiner.PdfMerger')
    def test_combine_files(self, mock_merger_class, temp_dir):
        """Test combining PDF files."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger
        
        # Create dummy PDF files
        pdf_files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.pdf")
            with open(file_path, "wb") as f:
                f.write(b"%PDF-1.4\n")  # Minimal PDF header
            pdf_files.append(file_path)
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        combiner = PdfCombiner()
        result = combiner.combine_files(pdf_files, output_file)
        
        assert result == output_file
        assert mock_merger.append.call_count == 3
        mock_merger.write.assert_called_once_with(output_file)
        mock_merger.close.assert_called_once()
    
    @patch('src.docconvert.converters.pdf_combiner.PdfMerger')
    def test_combine_files_with_metadata(self, mock_merger_class, temp_dir):
        """Test combining PDF files with metadata."""
        mock_merger = MagicMock()
        mock_merger_class.return_value = mock_merger
        
        # Create dummy PDF files
        pdf_files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.pdf")
            with open(file_path, "wb") as f:
                f.write(b"%PDF-1.4\n")  # Minimal PDF header
            pdf_files.append(file_path)
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        options = {
            "metadata": {
                "title": "Test Document",
                "author": "Test Author",
                "subject": "Test Subject",
                "keywords": "test, document"
            }
        }
        
        combiner = PdfCombiner(options)
        result = combiner.combine_files(pdf_files, output_file)
        
        assert result == output_file
        assert mock_merger.add_metadata.call_count == 4
        assert mock_merger.append.call_count == 3
        mock_merger.write.assert_called_once_with(output_file)
        mock_merger.close.assert_called_once()
    
    def test_combine_files_nonexistent(self, temp_dir):
        """Test combining nonexistent PDF files."""
        pdf_files = [
            os.path.join(temp_dir, "nonexistent1.pdf"),
            os.path.join(temp_dir, "nonexistent2.pdf")
        ]
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        combiner = PdfCombiner()
        
        with pytest.raises(FileNotFoundError):
            combiner.combine_files(pdf_files, output_file)
    
    @patch('src.docconvert.converters.pdf_combiner.glob.glob')
    @patch('src.docconvert.converters.pdf_combiner.PdfCombiner.combine_files')
    def test_combine_directory(self, mock_combine_files, mock_glob, temp_dir):
        """Test combining PDF files in a directory."""
        pdf_files = [
            os.path.join(temp_dir, "test1.pdf"),
            os.path.join(temp_dir, "test2.pdf"),
            os.path.join(temp_dir, "test3.pdf")
        ]
        mock_glob.return_value = pdf_files
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        # Mock the combine_files method to return the output file path
        mock_combine_files.return_value = output_file
        
        combiner = PdfCombiner()
        result = combiner.combine_directory(temp_dir, output_file)
        
        assert result == output_file
        mock_glob.assert_called_once_with(os.path.join(temp_dir, "*.pdf"))
        mock_combine_files.assert_called_once_with(pdf_files, output_file)
    
    @patch('src.docconvert.converters.pdf_combiner.glob.glob')
    @patch('src.docconvert.converters.pdf_combiner.PdfCombiner.combine_files')
    def test_combine_directory_with_order(self, mock_combine_files, mock_glob, temp_dir):
        """Test combining PDF files in a directory with a specific order."""
        pdf_files = [
            os.path.join(temp_dir, "test1.pdf"),
            os.path.join(temp_dir, "test2.pdf"),
            os.path.join(temp_dir, "test3.pdf")
        ]
        mock_glob.return_value = pdf_files
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        # Specify a different order
        file_order = ["test3.pdf", "test1.pdf", "test2.pdf"]
        
        # Mock the combine_files method to return the output file path
        mock_combine_files.return_value = output_file
        
        # Mock os.path.exists to return True for all files
        with patch('os.path.exists', return_value=True):
            combiner = PdfCombiner()
            result = combiner.combine_directory(temp_dir, output_file, file_order=file_order)
        
        assert result == output_file
        mock_glob.assert_called_once_with(os.path.join(temp_dir, "*.pdf"))
        
        # Check that the files were passed in the correct order
        expected_files = [
            os.path.join(temp_dir, "test3.pdf"),
            os.path.join(temp_dir, "test1.pdf"),
            os.path.join(temp_dir, "test2.pdf")
        ]
        mock_combine_files.assert_called_once_with(expected_files, output_file)
    
    def test_combine_directory_nonexistent(self, temp_dir):
        """Test combining PDF files in a nonexistent directory."""
        input_dir = os.path.join(temp_dir, "nonexistent")
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        combiner = PdfCombiner()
        
        with pytest.raises(FileNotFoundError):
            combiner.combine_directory(input_dir, output_file)


@pytest.mark.unit
class TestCombinePdfs:
    """Tests for the combine_pdfs function."""
    
    @patch('src.docconvert.converters.pdf_combiner.PdfCombiner')
    def test_combine_files(self, mock_combiner_class, temp_dir):
        """Test combining PDF files."""
        mock_combiner = MagicMock()
        mock_combiner.combine_files.return_value = "combined.pdf"
        mock_combiner_class.return_value = mock_combiner
        
        pdf_files = [
            os.path.join(temp_dir, "test1.pdf"),
            os.path.join(temp_dir, "test2.pdf"),
            os.path.join(temp_dir, "test3.pdf")
        ]
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        result = combine_pdfs(pdf_files, output_file)
        
        assert result == "combined.pdf"
        mock_combiner_class.assert_called_once_with(None)
        mock_combiner.combine_files.assert_called_once_with(pdf_files, output_file)
    
    @patch('src.docconvert.converters.pdf_combiner.PdfCombiner')
    def test_combine_directory(self, mock_combiner_class, temp_dir):
        """Test combining PDF files in a directory."""
        mock_combiner = MagicMock()
        mock_combiner.combine_directory.return_value = "combined.pdf"
        mock_combiner_class.return_value = mock_combiner
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        result = combine_pdfs(temp_dir, output_file)
        
        assert result == "combined.pdf"
        mock_combiner_class.assert_called_once_with(None)
        mock_combiner.combine_directory.assert_called_once_with(temp_dir, output_file, file_pattern='*.pdf', file_order=None)
    
    @patch('src.docconvert.converters.pdf_combiner.PdfCombiner')
    def test_combine_directory_with_options(self, mock_combiner_class, temp_dir):
        """Test combining PDF files in a directory with options."""
        mock_combiner = MagicMock()
        mock_combiner.combine_directory.return_value = "combined.pdf"
        mock_combiner_class.return_value = mock_combiner
        
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        options = {
            "file_order": ["test3.pdf", "test1.pdf", "test2.pdf"],
            "metadata": {
                "title": "Test Document"
            }
        }
        
        result = combine_pdfs(temp_dir, output_file, options)
        
        assert result == "combined.pdf"
        mock_combiner_class.assert_called_once_with(options)
        mock_combiner.combine_directory.assert_called_once_with(
            temp_dir, output_file, file_pattern='*.pdf', file_order=options["file_order"]
        )
    
    def test_combine_pdfs_invalid_input(self, temp_dir):
        """Test combining PDF files with invalid input."""
        output_file = os.path.join(temp_dir, "combined.pdf")
        
        with pytest.raises(ValueError):
            combine_pdfs(123, output_file)  # Invalid input type
