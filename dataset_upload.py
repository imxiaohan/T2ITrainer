import os
import zipfile
import tarfile
import shutil
import json
import re
from pathlib import Path
import gradio as gr

class DatasetUploader:
    def __init__(self, datasets_dir="datasets"):
        self.datasets_dir = Path(datasets_dir)
        self.datasets_dir.mkdir(exist_ok=True)
        self.supported_formats = {'.zip', '.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz'}
        
    def get_next_sequence_number(self, dataset_name):
        """Get the next sequence number for a dataset name"""
        pattern = re.compile(rf"^{re.escape(dataset_name)}_(\d+)$")
        max_num = 0
        
        for item in self.datasets_dir.iterdir():
            if item.is_dir():
                match = pattern.match(item.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))
        
        return max_num + 1
    
    def validate_dataset_structure(self, dataset_path):
        """Validate if the dataset has the required structure
        
        Supports both standard format and kontext paired format:
        - Standard: image1.jpg + image1.txt
        - Kontext: 01_R.png + 01_T.png + 01_T.txt (paired reference and target images)
        """
        dataset_path = Path(dataset_path)
        
        # Check for required structure
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        text_extensions = {'.txt', '.caption'}
        
        image_files = []
        text_files = []
        
        for file in dataset_path.rglob('*'):
            if file.is_file() and not file.name.startswith('.'):
                if file.suffix.lower() in image_extensions:
                    image_files.append(file)
                elif file.suffix.lower() in text_extensions:
                    text_files.append(file)
        
        if not image_files:
            return False, "No image files found in dataset"
        
        # Check for kontext paired format (XX_R.xxx, XX_T.xxx files)
        kontext_pattern = re.compile(r'^(\d+)_[RT]\.(png|jpg|jpeg|webp)$', re.IGNORECASE)
        kontext_images = [f for f in image_files if kontext_pattern.match(f.name)]
        
        if kontext_images:
            # Kontext format detected - validate paired structure
            base_names = set()
            for img in kontext_images:
                match = kontext_pattern.match(img.name)
                if match:
                    base_names.add(match.group(1))
            
            # Check for required pairs: each number should have _R and _T files
            missing_pairs = []
            for base in base_names:
                has_r = any(f.name.lower() == f"{base}_r.png" or f"{base}_r.jpg" for f in kontext_images)
                has_t = any(f.name.lower() == f"{base}_t.png" or f"{base}_t.jpg" for f in kontext_images)
                
                if not (has_r and has_t):
                    missing_pairs.append(base)
            
            if missing_pairs:
                return False, f"Kontext format: missing R/T pairs for bases: {missing_pairs}"
            
            # Check for corresponding text files for T images
            kontext_texts = [f for f in text_files if re.match(r'^\d+_T\.txt$', f.name, re.IGNORECASE)]
            expected_texts = [f"{base}_T.txt" for base in base_names]
            missing_texts = [txt for txt in expected_texts if not any(f.name.lower() == txt.lower() for f in kontext_texts)]
            
            if missing_texts:
                return False, f"Kontext format: missing text files: {missing_texts}"
            
            return True, f"Valid kontext dataset: {len(base_names)} pairs ({len(kontext_images)} images, {len(kontext_texts)} text files)"
        
        else:
            # Standard format - validate image-text pairs
            if not text_files:
                return False, "No text/caption files found in dataset"
            
            # Check if images have corresponding text files
            image_stems = {img.stem for img in image_files}
            text_stems = {txt.stem for txt in text_files}
            
            missing_texts = image_stems - text_stems
            if missing_texts:
                return False, f"Missing text files for images: {len(missing_texts)} images without captions"
            
            return True, f"Valid standard dataset: {len(image_files)} images, {len(text_files)} text files"
    
    def extract_archive(self, archive_path, extract_to):
        """Extract archive file to specified directory"""
        archive_path = Path(archive_path)
        extract_to = Path(extract_to)
        
        try:
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix.lower() in {'.tar', '.gz', '.bz2', '.xz'}:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                return False, "Unsupported archive format"
            
            return True, "Archive extracted successfully"
        except Exception as e:
            return False, f"Error extracting archive: {str(e)}"
    
    def upload_dataset(self, file_obj, dataset_name):
        """Upload and process a dataset archive"""
        if not file_obj:
            return None, "No file provided"
        
        if not dataset_name:
            return None, "Please provide a dataset name"
        
        # Handle gradio file object
        if hasattr(file_obj, 'name'):
            file_path = Path(file_obj.name)
        else:
            file_path = Path(str(file_obj))
        
        # Check file extension
        file_extension = ''.join(file_path.suffixes).lower()
        if file_extension not in self.supported_formats:
            supported = ', '.join(self.supported_formats)
            return None, f"Unsupported format. Supported formats: {supported}"
        
        # Get next sequence number
        sequence_num = self.get_next_sequence_number(dataset_name)
        dataset_dir_name = f"{dataset_name}_{sequence_num:03d}"
        dataset_path = self.datasets_dir / dataset_dir_name
        
        try:
            # Create dataset directory
            dataset_path.mkdir(exist_ok=True)
            
            # Copy uploaded file to temp location
            temp_archive = dataset_path / f"temp{file_extension}"
            shutil.copy2(file_path, temp_archive)
            
            # Extract archive
            extract_temp = dataset_path / "extracted"
            extract_temp.mkdir(exist_ok=True)
            
            success, message = self.extract_archive(temp_archive, extract_temp)
            if not success:
                shutil.rmtree(dataset_path)
                return None, message
            
            # Remove temp archive
            temp_archive.unlink()
            
            # Find the actual dataset content (handle nested directories)
            actual_content = extract_temp
            content_items = list(extract_temp.iterdir())
            
            # If extracted content has only one directory, use that as root
            if len(content_items) == 1 and content_items[0].is_dir():
                actual_content = content_items[0]
            
            # Move content to dataset root
            for item in actual_content.iterdir():
                shutil.move(str(item), str(dataset_path))
            
            # Remove empty extracted directory
            shutil.rmtree(extract_temp)
            
            # Validate dataset structure
            is_valid, validation_message = self.validate_dataset_structure(dataset_path)
            if not is_valid:
                shutil.rmtree(dataset_path)
                return None, f"Dataset validation failed: {validation_message}"
            
            # Return the path to be used for train_data_dir
            return str(dataset_path), f"Successfully uploaded {dataset_name}_{sequence_num:03d}: {validation_message}"
            
        except Exception as e:
            if dataset_path.exists():
                shutil.rmtree(dataset_path)
            return None, f"Error processing dataset: {str(e)}"

# Global instance
dataset_uploader = DatasetUploader()

def upload_dataset_interface(file_input, dataset_name):
    """Gradio interface function for dataset upload"""
    path, message = dataset_uploader.upload_dataset(file_input, dataset_name)
    return path, message

def add_dataset_upload_tab(demo):
    """Add dataset upload tab to the existing Gradio interface"""
    with gr.Tab("Dataset Upload"):
        gr.Markdown("""
        ## Upload Training Dataset
        Upload your dataset archive (zip, tar, tar.gz, etc.) and it will be automatically extracted and validated.
        """)
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(
                    label="Dataset Archive",
                    file_types=[".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2", ".tar.xz", ".txz"]
                )
                dataset_name = gr.Textbox(
                    label="Dataset Name",
                    placeholder="Enter a name for this dataset (e.g., my_dataset)"
                )
                upload_btn = gr.Button("Upload Dataset", variant="primary")
            
            with gr.Column():
                upload_output = gr.Textbox(label="Upload Status", interactive=False)
                dataset_path = gr.Textbox(label="Dataset Path", interactive=False)
                
        upload_btn.click(
            fn=upload_dataset_interface,
            inputs=[file_input, dataset_name],
            outputs=[dataset_path, upload_output]
        )
        
        gr.Markdown("""
        ### Dataset Requirements:
        - Archive must contain image files (jpg, jpeg, png, bmp, webp) and corresponding text files (txt, caption)
        - Each image should have a text file with the same name containing the caption
        - Example structure:
          ```
          dataset/
          ├── image1.jpg
          ├── image1.txt
          ├── image2.png
          ├── image2.txt
          └── ...
          ```
        """)

if __name__ == "__main__":
    # Test the uploader
    uploader = DatasetUploader()
    print("Dataset uploader initialized")