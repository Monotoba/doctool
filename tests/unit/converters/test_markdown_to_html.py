"""
Unit tests for the Markdown to HTML converter module.
"""

import os
import pytest
from src.docconvert.converters.markdown_to_html import MarkdownToHtmlConverter, convert_md_to_html


@pytest.mark.unit
class TestMarkdownToHtmlConverter:
    """Tests for the MarkdownToHtmlConverter class."""
    
    def test_init(self):
        """Test initialization of MarkdownToHtmlConverter."""
        converter = MarkdownToHtmlConverter()
        assert converter.options == {}
        assert converter.html_template is not None
        assert converter.default_css is not None
        
        options = {"test": "option"}
        converter = MarkdownToHtmlConverter(options)
        assert converter.options == options
    
    def test_convert_text(self):
        """Test converting Markdown text to HTML."""
        converter = MarkdownToHtmlConverter()
        
        md_text = "# Test Heading\n\nThis is a test paragraph."
        html_text = converter.convert_text(md_text)
        
        assert "<h1>Test Heading</h1>" in html_text
        assert "<p>This is a test paragraph.</p>" in html_text
    
    def test_convert_file(self, sample_md_file, temp_dir):
        """Test converting a Markdown file to HTML."""
        output_file = os.path.join(temp_dir, "output.html")
        
        converter = MarkdownToHtmlConverter()
        result = converter.convert_file(sample_md_file, output_file)
        
        assert result == output_file
        assert os.path.exists(output_file)
        
        with open(output_file, "r", encoding="utf-8") as f:
            html_content = f.read()
            assert "<!DOCTYPE html>" in html_content
            assert "<title>" in html_content
            assert "<h1>Test Document</h1>" in html_content
    
    def test_convert_file_nonexistent(self, temp_dir):
        """Test converting a nonexistent Markdown file."""
        input_file = os.path.join(temp_dir, "nonexistent.md")
        output_file = os.path.join(temp_dir, "output.html")
        
        converter = MarkdownToHtmlConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.convert_file(input_file, output_file)
    
    def test_convert_file_with_css(self, sample_md_file, temp_dir):
        """Test converting a Markdown file to HTML with custom CSS."""
        output_file = os.path.join(temp_dir, "output.html")
        css_file = os.path.join(temp_dir, "custom.css")
        
        # Create a custom CSS file
        custom_css = "body { font-family: Arial; color: blue; }"
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(custom_css)
        
        options = {"css": css_file}
        converter = MarkdownToHtmlConverter(options)
        result = converter.convert_file(sample_md_file, output_file)
        
        assert result == output_file
        assert os.path.exists(output_file)
        
        with open(output_file, "r", encoding="utf-8") as f:
            html_content = f.read()
            assert custom_css in html_content
    
    def test_convert_directory(self, temp_dir):
        """Test converting a directory of Markdown files to HTML."""
        # Create multiple Markdown files
        md_files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Test Document {i}\n\nThis is test document {i}.")
            md_files.append(file_path)
        
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        converter = MarkdownToHtmlConverter()
        result = converter.convert_directory(temp_dir, output_dir)
        
        assert len(result) == 3
        for i in range(3):
            html_file = os.path.join(output_dir, f"test{i}.html")
            assert os.path.exists(html_file)
            assert html_file in result
    
    def test_convert_directory_nonexistent(self, temp_dir):
        """Test converting a nonexistent directory."""
        input_dir = os.path.join(temp_dir, "nonexistent")
        output_dir = os.path.join(temp_dir, "output")
        
        converter = MarkdownToHtmlConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.convert_directory(input_dir, output_dir)


@pytest.mark.unit
class TestConvertMdToHtml:
    """Tests for the convert_md_to_html function."""
    
    def test_convert_file(self, sample_md_file, temp_dir):
        """Test converting a Markdown file to HTML."""
        output_file = os.path.join(temp_dir, "output.html")
        
        result = convert_md_to_html(sample_md_file, output_file)
        
        assert result == output_file
        assert os.path.exists(output_file)
    
    def test_convert_directory(self, temp_dir):
        """Test converting a directory of Markdown files to HTML."""
        # Create multiple Markdown files
        md_files = []
        for i in range(3):
            file_path = os.path.join(temp_dir, f"test{i}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Test Document {i}\n\nThis is test document {i}.")
            md_files.append(file_path)
        
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        result = convert_md_to_html(temp_dir, output_dir)
        
        assert len(result) == 3
        for i in range(3):
            html_file = os.path.join(output_dir, f"test{i}.html")
            assert os.path.exists(html_file)
            assert html_file in result