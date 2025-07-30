# Dataset Upload Feature

This feature adds the ability to upload dataset archives directly through the web interface, with automatic extraction and validation.

## Features

1. **Support for multiple archive formats**: zip, tar, tar.gz, tgz, tar.bz2, tbz2, tar.xz, txz
2. **Automatic extraction**: Archives are automatically extracted to the datasets directory
3. **Dataset validation**: Checks if the dataset contains valid image-text pairs
4. **Sequential naming**: Uploaded datasets are saved as `dataset_name_001`, `dataset_name_002`, etc.
5. **Integration with UI**: New "Dataset Upload" tab in the web interface

## Usage

### Through Web Interface
1. Run the application: `python ui.py`
2. Open the web interface in your browser
3. Navigate to the "Dataset Upload" tab
4. Select your dataset archive file
5. Enter a dataset name
6. Click "Upload Dataset"
7. The dataset will be extracted and validated automatically
8. The dataset path will be displayed and can be used as `train_data_dir`

### Dataset Structure Requirements

The uploader supports two dataset formats:

#### 1. Standard Format (for regular training)
Your dataset archive should contain:
- **Image files**: .jpg, .jpeg, .png, .bmp, .webp
- **Text files**: .txt or .caption files with the same name as corresponding images

Example structure:
```
dataset.zip
├── image1.jpg
├── image1.txt
├── image2.png
├── image2.txt
└── ...
```

#### 2. Kontext Paired Format (for kontext training)
For kontext (context-aware) training, use the paired format:
- **Reference images**: `01_R.png`, `02_R.png`, etc.
- **Target images**: `01_T.png`, `02_T.png`, etc.
- **Text files**: `01_T.txt`, `02_T.txt`, etc. (captions for target images)

Example structure:
```
kontext_dataset.zip
├── 01_R.png      # Reference/context image
├── 01_T.png      # Target image
├── 01_T.txt      # Caption for target image
├── 02_R.png
├── 02_T.png
├── 02_T.txt
└── ...
```

### Programmatic Usage

You can also use the `DatasetUploader` class programmatically:

```python
from dataset_upload import DatasetUploader

uploader = DatasetUploader(datasets_dir="datasets")
path, message = uploader.upload_dataset("path/to/dataset.zip", "my_dataset")
print(f"Dataset uploaded to: {path}")
```

## Directory Structure

Uploaded datasets are stored in the `datasets/` directory with sequential numbering:
```
datasets/
├── my_dataset_001/
├── my_dataset_002/
├── another_dataset_001/
└── ...
```

## Validation Rules

The system validates datasets based on:
1. Presence of image files
2. Presence of text/caption files
3. Each image has a corresponding text file with the same name
4. Valid file extensions for images and text files

## Error Handling

Common issues and solutions:
- **"No image files found"**: Your archive doesn't contain any supported image formats
- **"No text files found"**: Missing caption files
- **"Missing text files for images"**: Some images don't have corresponding text files
- **"Unsupported format"**: Use supported archive formats (zip, tar, etc.)