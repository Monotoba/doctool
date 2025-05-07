"""
Unit tests for the HTML to PDF converter module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.docconvert.converters.html_to_pdf import HtmlToPdfConverter, convert_html_to_pdf


@pytest.mark.unit
class TestHtmlToPdfConverter:
    """Tests for the HtmlToPdfConverter class."""
    
    def test_init(self):
        """Test initialization of HtmlToPdfConverter."""
        converter = HtmlToPdfConverter()
        assert converter.options == {}
        
        options = {"test": "option"}
        converter = HtmlToPdfConverter(options)
        assert converter.options == options
    
    @patch('src.docconvert.converters.html_to_pdf.HTML')
    def test_convert_file(self, mock_html_class, sample_html_file, temp_dir):
        """Test converting an HTML file to PDF."""
        mock_html = MagicMock()
        mock_html_class.return_value = mock_html
        
        output_file = os.path.join(temp_dir, "output.pdf")
        
        converter = HtmlToPdfConverter()
        result = converter.convert_file(sample_html_file, output_file)
        
        assert result == output_file
        mock_html_class.assert_called_once_with(filename=sample_html_file)
        mock_html.write_pdf.assert_called_once_with(output_file, stylesheets=[])
    
    def test_convert_file_nonexistent(self, temp_dir):
        """Test converting a nonexistent HTML file."""
        input_file = os.path.join(temp_dir, "nonexistent.html")
        output_file = os.path.join(temp_dir, "output.pdf")
        
        converter = HtmlToPdfConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.convert_file(input_file, output_file)
    
    @patch('src.docconvert.converters.html_to_pdf.HTML')
    @patch('src.docconvert.converters.html_to_pdf.CSS')
    def test_convert_file_with_css(self, mock_css_class, mock_html_class, sample_html_file, temp_dir):
        """Test converting an HTML file to PDF with custom CSS."""
        mock_html = MagicMock()
        mock_html_class.return_value = mock_html
        
        mock_css = MagicMock()
        mock_css_class.return_value = mock_css
        
        output_file = os.path.join(temp_dir, "output.pdf")
        css_file = os.path.join(temp_dir, "custom.css")
        
        # Create a custom CSS file
        with open(css_file, "w", encoding="utf-8") as f:
            f.write("body { font-family: Arial; color: blue; }")
        
        options = {"css": css_file}
        converter = HtmlToPdfConverter(options)
        result = converter.convert_file(sample_html_file, output_file)
        
        assert result == output_file
        mock_html_class.assert_called_once_with(filename=sample_html_file)
        mock_css_class.assert_called_once_with(filename=css_file)
        mock_html.write_pdf.assert_called_once_with(output_file, stylesheets=[mock_css])
    
    @patch('src.docconvert.converters.html_to_pdf.glob.glob')
    @patch('src.docconvert.converters.html_to_pdf.HtmlToPdfConverter.convert_file')
    def test_convert_directory(self, mock_convert_file, mock_glob, temp_dir):
        """Test converting a directory of HTML files to PDF."""
        html_files = [
            os.path.join(temp_dir, "test1.html"),
            os.path.join(temp_dir, "test2.html"),
            os.path.join(temp_dir, "test3.html")
        ]
        mock_glob.return_value = html_files
        
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Mock the convert_file method to return the output file path
        def side_effect(input_file, output_file):
            return output_file
        
        mock_convert_file.side_effect = side_effect
        
        converter = HtmlToPdfConverter()
        result = converter.convert_directory(temp_dir, output_dir)
        
        assert len(result) == 3
        mock_glob.assert_called_once_with(os.path.join(temp_dir, "*.html"))
        assert mock_convert_file.call_count == 3
    
    def test_convert_directory_nonexistent(self, temp_dir):
        """Test converting a nonexistent directory."""
        input_dir = os.path.join(temp_dir, "nonexistent")
        output_dir = os.path.join(temp_dir, "output")
        
        converter = HtmlToPdfConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.convert_directory(input_dir, output_dir)


@pytest.mark.unit
class TestConvertHtmlToPdf:
    """Tests for the convert_html_to_pdf function."""
    
    @patch('src.docconvert.converters.html_to_pdf.HtmlToPdfConverter')
    def test_convert_file(self, mock_converter_class, sample_html_file, temp_dir):
        """Test converting an HTML file to PDF."""
        mock_converter = MagicMock()
        mock_converter.convert_file.return_value = "output.pdf"
        mock_converter_class.return_value = mock_converter
        
        output_file = os.path.join(temp_dir, "output.pdf")
        
        result = convert_html_to_pdf(sample_html_file, output_file)
        
        assert result == "output.pdf"
        mock_converter_class.assert_called_once_with(None)
        mock_converter.convert_file.assert_called_once_with(sample_html_file, output_file)
    
    @patch('src.docconvert.converters.html_to_pdf.HtmlToPdfConverter')
    def test_convert_directory(self, mock_converter_class, temp_dir):
        """Test converting a directory of HTML files to PDF."""
        mock_converter = MagicMock()
        mock_converter.convert_directory.return_value = ["output1.pdf", "output2.pdf"]
        mock_converter_class.return_value = mock_converter
        
        output_dir = os.path.join(temp_dir, "output")
        
        result = convert_html_to_pdf(temp_dir, output_dir)
        
        assert result == ["output1.pdf", "output2.pdf"]
        mock_converter_class.assert_called_once_with(None)
        mock_converter.convert_directory.assert_called_once_with(temp_dir, output_dir, file_pattern="*.html")