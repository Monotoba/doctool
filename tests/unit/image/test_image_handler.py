"""
Unit tests for the image handler module.
"""

import os
import pytest
import base64
from unittest.mock import patch, MagicMock
from src.docconvert.image.image_handler import ImageHandler, process_images


@pytest.mark.unit
class TestImageHandler:
    """Tests for the ImageHandler class."""
    
    def test_init(self):
        """Test initialization of ImageHandler."""
        handler = ImageHandler()
        assert handler.options == {}
        assert handler.supported_formats == ['jpg', 'jpeg', 'png', 'webp', 'svg']
        assert handler.embed_images is True
        
        options = {
            "formats": ["jpg", "png"],
            "embed": False
        }
        handler = ImageHandler(options)
        assert handler.options == options
        assert handler.supported_formats == ["jpg", "png"]
        assert handler.embed_images is False
    
    def test_process_image_nonexistent(self, temp_dir):
        """Test processing a nonexistent image file."""
        image_path = os.path.join(temp_dir, "nonexistent.png")
        
        handler = ImageHandler()
        
        with pytest.raises(FileNotFoundError):
            handler.process_image(image_path)
    
    def test_process_image_unsupported_format(self, temp_dir):
        """Test processing an image with an unsupported format."""
        image_path = os.path.join(temp_dir, "test.xyz")
        
        # Create a dummy file
        with open(image_path, "wb") as f:
            f.write(b"dummy data")
        
        handler = ImageHandler()
        
        with pytest.raises(ValueError):
            handler.process_image(image_path)
    
    def test_process_image_embed(self, sample_image_file):
        """Test processing an image file with embedding."""
        handler = ImageHandler({"embed": True})
        result = handler.process_image(sample_image_file)
        
        assert result.startswith("data:image/png;base64,")
    
    def test_process_image_no_embed(self, sample_image_file, temp_dir):
        """Test processing an image file without embedding."""
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        handler = ImageHandler({"embed": False})
        result = handler.process_image(sample_image_file, output_dir)
        
        assert os.path.exists(result)
        assert os.path.basename(result) == os.path.basename(sample_image_file)
    
    @patch('src.docconvert.image.image_handler.base64.b64encode')
    def test_get_data_uri(self, mock_b64encode, sample_image_file):
        """Test getting a data URI for an image file."""
        mock_b64encode.return_value = b"encoded_data"
        
        handler = ImageHandler()
        result = handler.get_data_uri(sample_image_file)
        
        assert result == "data:image/png;base64,encoded_data"
        mock_b64encode.assert_called_once()
    
    @patch('src.docconvert.image.image_handler.os.walk')
    def test_find_images_in_directory(self, mock_walk, temp_dir):
        """Test finding images in a directory."""
        mock_walk.return_value = [
            (temp_dir, [], ["test1.jpg", "test2.png", "test3.txt"])
        ]
        
        handler = ImageHandler()
        result = handler.find_images_in_directory(temp_dir)
        
        assert len(result) == 2
        assert os.path.join(temp_dir, "test1.jpg") in result
        assert os.path.join(temp_dir, "test2.png") in result
        assert os.path.join(temp_dir, "test3.txt") not in result
    
    def test_find_images_in_directory_nonexistent(self, temp_dir):
        """Test finding images in a nonexistent directory."""
        nonexistent_dir = os.path.join(temp_dir, "nonexistent")
        
        handler = ImageHandler()
        
        with pytest.raises(FileNotFoundError):
            handler.find_images_in_directory(nonexistent_dir)
    
    @patch('src.docconvert.image.image_handler.ImageHandler.find_images_in_directory')
    @patch('src.docconvert.image.image_handler.ImageHandler.process_image')
    def test_process_images_in_directory(self, mock_process_image, mock_find_images, temp_dir):
        """Test processing images in a directory."""
        image_files = [
            os.path.join(temp_dir, "test1.jpg"),
            os.path.join(temp_dir, "test2.png")
        ]
        mock_find_images.return_value = image_files
        
        # Mock the process_image method to return a data URI
        def side_effect(image_path, output_dir=None):
            return f"data:image/{os.path.splitext(image_path)[1][1:]};base64,dummy"
        
        mock_process_image.side_effect = side_effect
        
        output_dir = os.path.join(temp_dir, "output")
        
        handler = ImageHandler()
        result = handler.process_images_in_directory(temp_dir, output_dir)
        
        assert len(result) == 2
        assert image_files[0] in result
        assert image_files[1] in result
        assert result[image_files[0]].startswith("data:image/jpg;base64,")
        assert result[image_files[1]].startswith("data:image/png;base64,")
        mock_find_images.assert_called_once_with(temp_dir)
        assert mock_process_image.call_count == 2


@pytest.mark.unit
class TestProcessImages:
    """Tests for the process_images function."""
    
    @patch('src.docconvert.image.image_handler.ImageHandler')
    def test_process_single_image(self, mock_handler_class, sample_image_file):
        """Test processing a single image file."""
        mock_handler = MagicMock()
        mock_handler.process_image.return_value = "data:image/png;base64,dummy"
        mock_handler_class.return_value = mock_handler
        
        result = process_images(sample_image_file)
        
        assert result == "data:image/png;base64,dummy"
        mock_handler_class.assert_called_once_with(None)
        mock_handler.process_image.assert_called_once_with(sample_image_file, None)
    
    @patch('src.docconvert.image.image_handler.ImageHandler')
    def test_process_directory(self, mock_handler_class, temp_dir):
        """Test processing images in a directory."""
        mock_handler = MagicMock()
        mock_handler.process_images_in_directory.return_value = {
            "image1.jpg": "data:image/jpg;base64,dummy1",
            "image2.png": "data:image/png;base64,dummy2"
        }
        mock_handler_class.return_value = mock_handler
        
        output_dir = os.path.join(temp_dir, "output")
        
        result = process_images(temp_dir, output_dir)
        
        assert len(result) == 2
        assert "image1.jpg" in result
        assert "image2.png" in result
        mock_handler_class.assert_called_once_with(None)
        mock_handler.process_images_in_directory.assert_called_once_with(temp_dir, output_dir)
    
    @patch('src.docconvert.image.image_handler.ImageHandler')
    def test_process_multiple_images(self, mock_handler_class, temp_dir):
        """Test processing multiple image files."""
        mock_handler = MagicMock()
        
        # Mock the process_image method to return a data URI
        def side_effect(image_path, output_dir=None):
            ext = os.path.splitext(image_path)[1][1:]
            return f"data:image/{ext};base64,dummy"
        
        mock_handler.process_image.side_effect = side_effect
        mock_handler_class.return_value = mock_handler
        
        image_files = [
            os.path.join(temp_dir, "test1.jpg"),
            os.path.join(temp_dir, "test2.png")
        ]
        
        result = process_images(image_files)
        
        assert len(result) == 2
        assert image_files[0] in result
        assert image_files[1] in result
        assert result[image_files[0]] == "data:image/jpg;base64,dummy"
        assert result[image_files[1]] == "data:image/png;base64,dummy"
        mock_handler_class.assert_called_once_with(None)
        assert mock_handler.process_image.call_count == 2
    
    def test_process_images_invalid_input(self):
        """Test processing images with invalid input."""
        with pytest.raises(ValueError):
            process_images(123)  # Invalid input type