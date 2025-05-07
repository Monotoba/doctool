#!/usr/bin/env python3
"""
Image handler module.
Handles image processing and embedding for document conversion.
"""

import os
import base64
import mimetypes
from PIL import Image
from typing import Dict, Any, List, Optional, Union


class ImageHandler:
    """
    Handler for image processing and embedding.
    """
    
    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the image handler.
        
        Args:
            options: Optional image handling options
        """
        self.options = options or {}
        
        # Default supported image formats
        self.supported_formats = self.options.get('formats', ['jpg', 'jpeg', 'png', 'webp', 'svg'])
        
        # Whether to embed images in the output document
        self.embed_images = self.options.get('embed', True)
    
    def process_image(self, image_path: str, output_dir: Optional[str] = None) -> str:
        """
        Process an image file.
        
        Args:
            image_path: Path to the input image file
            output_dir: Optional output directory for processed images
            
        Returns:
            Path to the processed image file or data URI if embedding
            
        Raises:
            FileNotFoundError: If the input file does not exist
            ValueError: If the image format is not supported
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Get image format
        image_ext = os.path.splitext(image_path)[1].lower().lstrip('.')
        if image_ext not in self.supported_formats and image_ext != 'svg':
            raise ValueError(f"Unsupported image format: {image_ext}")
        
        # If embedding is enabled, return data URI
        if self.embed_images:
            return self.get_data_uri(image_path)
        
        # If output directory is specified, copy image to output directory
        if output_dir:
            import shutil
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            shutil.copy2(image_path, output_path)
            return output_path
        
        # Otherwise, return the original image path
        return image_path
    
    def get_data_uri(self, image_path: str) -> str:
        """
        Get data URI for an image file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Data URI string
            
        Raises:
            IOError: If there is an error reading the image file
        """
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                # Default to PNG if MIME type cannot be determined
                mime_type = 'image/png'
            
            # Handle SVG files differently
            if image_path.lower().endswith('.svg'):
                with open(image_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                return f"data:{mime_type};utf8,{svg_content}"
            
            # For other image formats, use base64 encoding
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            encoded_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_data}"
        except Exception as e:
            raise IOError(f"Error creating data URI for {image_path}: {e}")
    
    def find_images_in_directory(self, directory: str) -> List[str]:
        """
        Find all supported image files in a directory.
        
        Args:
            directory: Path to the directory
            
        Returns:
            List of image file paths
            
        Raises:
            FileNotFoundError: If the directory does not exist
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        image_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower().lstrip('.')
                if ext in self.supported_formats:
                    image_files.append(os.path.join(root, file))
        
        return image_files
    
    def process_images_in_directory(self, input_dir: str, output_dir: str) -> Dict[str, str]:
        """
        Process all supported image files in a directory.
        
        Args:
            input_dir: Path to the input directory
            output_dir: Path to the output directory
            
        Returns:
            Dictionary mapping original image paths to processed image paths
            
        Raises:
            FileNotFoundError: If the input directory does not exist
        """
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all supported image files
        image_files = self.find_images_in_directory(input_dir)
        
        # Process each image
        image_map = {}
        for image_file in image_files:
            try:
                processed_path = self.process_image(image_file, output_dir)
                image_map[image_file] = processed_path
                print(f"Processed image: {image_file} -> {processed_path}")
            except Exception as e:
                print(f"Error processing image {image_file}: {e}")
                import traceback
                traceback.print_exc()
        
        return image_map


def process_images(input_path: Union[str, List[str]], output_dir: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Union[str, Dict[str, str]]:
    """
    Process images for document conversion.
    
    Args:
        input_path: Path to the input image file or directory, or list of image file paths
        output_dir: Optional output directory for processed images
        options: Optional image handling options
        
    Returns:
        Path to the processed image file, or dictionary mapping original image paths to processed image paths
        
    Raises:
        FileNotFoundError: If the input file or directory does not exist
    """
    handler = ImageHandler(options)
    
    if isinstance(input_path, str):
        if os.path.isdir(input_path):
            return handler.process_images_in_directory(input_path, output_dir or input_path)
        else:
            return handler.process_image(input_path, output_dir)
    elif isinstance(input_path, list):
        image_map = {}
        for path in input_path:
            try:
                processed_path = handler.process_image(path, output_dir)
                image_map[path] = processed_path
            except Exception as e:
                print(f"Error processing image {path}: {e}")
                import traceback
                traceback.print_exc()
        return image_map
    else:
        raise ValueError("input_path must be a file path, directory path, or list of file paths")