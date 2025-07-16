# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Setup & Installation
```bash
# Automated setup (recommended)
./setup.sh    # Linux/macOS
setup.bat     # Windows

# Manual setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

### Running Training Interfaces
```bash
# Main training UIs by model type
python ui.py              # Kolors training
python ui_flux_fill.py    # Flux Fill training  
python ui_sd35.py         # SD3.5 Large training
python ui_slider.py       # Concept slider training
```

### Direct Training Scripts
```bash
python train_kolors_lora_ui.py
python train_flux_lora_ui.py
python train_flux_lora_ui_kontext.py
python train_sd3_lora_ui.py
```

## Architecture Overview

### Core Model Support
- **Kolors**: 11GB VRAM, Chinese text-to-image model
- **Flux Fill/Kontext**: 24GB VRAM, advanced inpainting models with NF4 support
- **SD3.5 Large**: 24GB VRAM, Stable Diffusion 3.5

### Directory Structure
```
├── flux/               # Flux-specific pipelines and utilities
├── kolors/             # Kolors model implementations
├── utils/              # Shared utilities across models
├── trainer/            # Core training framework
├── captioner/          # Image captioning tools
├── object_detection/   # Image preprocessing utilities
├── cache/              # Model embeddings and cached data
└── prepare_data/       # Dataset preparation scripts
```

### Key Entry Points
- **UI Layer**: `ui.py`, `ui_flux_fill.py`, `ui_sd35.py` - Gradio interfaces
- **Training Layer**: `train_*_lora_ui.py` - Direct training scripts
- **Configuration**: `config.json` - Training parameters
- **Model Management**: Download scripts in README.md

### Model-Specific Configurations
Each model type has dedicated configuration:
- Kolors: Uses `kolors_models/` directory
- Flux: Uses `flux_models/fill/` or `flux_models/kontext/`
- SD3.5: Uses `sd3.5L/` directory

### Training Parameters
Key VRAM optimization settings:
- `blocks_to_swap`: Higher values reduce VRAM usage
- `mixed_precision`: bf16/fp16 for memory efficiency
- NF4 quantization available for Flux models

### Model Downloads
```bash
# Kolors
huggingface-cli download Kwai-Kolors/Kolors --local-dir kolors_models/

# Flux NF4 (low VRAM)
huggingface-cli download lrzjason/flux-fill-nf4 --local-dir flux_models/fill/
huggingface-cli download lrzjason/flux-kontext-nf4 --local-dir flux_models/kontext/

# SD3.5
huggingface-cli download stabilityai/stable-diffusion-3.5-large --local-dir sd3.5L/
```