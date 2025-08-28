# T2ITrainer 模型训练手册

## 项目概述
T2ITrainer 是一个功能完整的文本到图像模型 LoRA (Low-Rank Adaptation) 训练框架，支持多种先进的模型架构，包括 Kolors、Flux、Qwen Image、Stable Diffusion 3 和 Hunyuan DiT。项目提供了丰富的训练模式和配置选项，满足不同训练需求。

## 训练脚本完整列表

| 训练脚本 | 主要功能 | UI界面 | 配置文件 |
|---------|---------|-----------|----------|
| train_qwen_image.py | Qwen图像模型的LoRA权重 | `ui_flux_fill.py` | [训练参数](doc/training/train_qwen_image_parameters.md) |
| train_qwen_image_edit.py | Qwen图像编辑模型的LoRA权重 | `ui_flux_fill.py` | [训练参数](doc/training/train_qwen_image_edit_parameters.md) |
| train_flux_lora_ui_kontext_new.py | Flux Kontext模型的LoRA权重(新版支持多图配置) | `ui_flux_fill.py` | [训练参数](doc/training/train_flux_kontext_lora_new_parameters.md) |
| train_flux_lora_ui_kontext.py | Flux Kontext模型的LoRA权重 | `ui_flux_fill.py` | [训练参数](doc/training/train_flux_lora_kontext_parameters.md) |
 train_flux_lora_ui.py | 555 | `ui_flux_fill.py` | [训练参数] |
| train_flux_lora_ui_kontext_slider.py | 444 | `ui_flux_fill.py` | [训练参数] |
| train_flux_lora_ui_with_mask.py | 555 | `ui_flux_fill.py` | [训练参数] |
| train_sd3_lora_ui.py | 666 | `ui_sd35.py` | [训练参数] |
| train_kolors_lora_ui.py | Kolors标准LoRA训练 | `ui.py` | [训练参数](doc/training/train_kolors_lora_parameters.md) |
| train_kolors_slider.py | 专门用于概念编辑的滑块训练脚本，通过正负样本对来训练Kolors的LoRA模型 | `ui_slider.py` | [训练参数](doc/training/train_kolors_slider_parameters.md) |
| train_hunyuan_lora_ui.py | 777 | - | [训练参数] |

## 训练脚本启动方法详解

### 1. Qwen系列训练
```bash
# 图像生成训练
python train_qwen_image.py --config_path config_qwen_single.json

# 图像编辑训练
python train_qwen_image_edit.py --config_path config_qwen_edit_pairs.json
```

### 2. Flux系列训练
```bash
# Flux LoRA训练
python train_flux_lora_ui.py --config_path config.json

# Flux Kontext LoRA训练
python train_flux_lora_ui_kontext.py --config_path config.json

# Flux Kontext LoRA训练新版
python train_flux_lora_ui_kontext_new.py --config_path config_new_pairs.json

# 带掩码条件训练
python train_flux_lora_ui_with_mask.py --config_path config.json

# 上下文滑块训练
python train_flux_lora_ui_kontext_slider.py --config_path config.json
```

### 3. Stable Diffusion 3训练
```bash
# SD3 LoRA训练
python train_sd3_lora_ui.py --config_path config.json
```

### 4. Kolors系列训练
```bash
# 标准LoRA训练
python train_kolors_lora_ui.py --config_path config.json

# 滑块训练
python train_kolors_slider.py --config_path config_slider.json
```

### 5. 其他模型训练
```bash
# Hunyuan DiT训练（旧版本）
python old/train_hunyuan_lora_ui.py --config_path config.json
```

## 模型架构详细对比

| 模型 | 文本编码器 | 主要特点 | 适用场景 | 内存需求 | 训练速度 |
|------|------------|----------|----------|----------|----------|
| **Kolors** | ChatGLM | 中文优化，桶采样，梯度检查点 | 中文图像生成，低显存训练 | 8-16GB | 中等 |
| **Flux** | CLIP+T5 | 流匹配，内存优化，块交换 | 高质量图像生成，上下文训练 | 16-24GB | 快 |
| **Qwen Image** | Qwen2.5-VL | 多模态理解，编辑任务 | 图像编辑，多图像训练 | 20-32GB | 快 |
| **SD3** | CLIP | Transformer架构，流匹配 | 最新SD架构，高质量生成 | 24-40GB | 中等 |
| **Hunyuan DiT** | BERT+MT5 | DiT架构，中文优化 | 中文生成，扩散变换器 | 16-32GB | 中等 |

## 训练模式详解

### 1. 标准LoRA训练
- **适用场景**: 基础风格/概念学习
- **数据要求**: 单图像+文本描述
- **训练目标**: 学习特定风格或概念
- **优势**: 简单高效，资源需求低

### 2. 上下文感知训练
- **适用场景**: 需要参考图像的训练
- **数据要求**: 目标图像+参考图像+文本
- **训练目标**: 学习图像间的转换关系
- **优势**: 更好的控制性和一致性

### 3. 滑块训练
- **适用场景**: 属性控制和对比学习
- **数据要求**: 正负样本对+属性标注
- **训练目标**: 学习属性的连续变化
- **优势**: 精确的属性控制，可调节强度

### 4. 掩码条件训练
- **适用场景**: 部分图像生成/编辑
- **数据要求**: 完整图像+掩码+文本
- **训练目标**: 学习条件生成
- **优势**: 支持局部编辑，保持一致性

