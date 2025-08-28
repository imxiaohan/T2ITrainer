# Flux Fill 配置文件参数说明文档

本文档详细介绍了 `config_flux_fill.json` 配置文件的所有参数，用于训练Flux模型的LoRA权重以进行图像填充（对象移除）任务。

## 配置文件使用方法

### 基础使用命令
```bash
# 使用JSON配置文件训练
python train_flux_lora_ui_with_mask.py --config_path=config_flux_fill.json
```

## 参数详细说明

### 模型和路径参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `pretrained_model_name_or_path` | 预训练模型路径或HuggingFace模型标识符 | `"black-forest-labs/FLUX.1-dev"` | 任意有效的模型路径或HF模型ID |
| `output_dir` | 模型预测结果和检查点的输出目录 | `"output/flux-fill"` | 任意有效的目录路径 |
| `model_path` | 从文件加载模型的独立路径 | `null` | 任意有效的模型文件路径 |
| `train_data_dir` | 训练数据图像文件夹 | `"data/flux-fill"` | 任意有效的目录路径 |
| `config_path` | JSON配置文件路径 | `"config_flux_fill.json"` | 任意有效的配置文件路径 |

### 训练超参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `train_batch_size` | 训练数据加载器的批次大小（每个设备） | `1` | 正整数 |
| `num_train_epochs` | 训练轮数 | `10` | 正整数 |
| `learning_rate` | 初始学习率（热身期后） | `1e-4` | 正浮点数 |
| `gradient_accumulation_steps` | 执行反向/更新步骤前累积的更新步数 | `1` | 正整数 |
| `gradient_checkpointing` | 是否使用梯度检查点以节省内存 | `true` | `true`, `false` |
| `repeats` | 训练数据的重复次数 | `10` | 正整数 |

### 优化器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `optimizer` | 要使用的优化器类型 | `"AdamW"` | `"AdamW"`, `"prodigy"` |
| `lr_scheduler` | 要使用的调度器类型 | `"constant"` | `"linear"`, `"cosine"`, `"cosine_with_restarts"`, `"polynomial"`, `"constant"`, `"constant_with_warmup"` |
| `lr_warmup_steps` | 学习率调度器的预热步数 | `50` | 非负整数 |
| `cosine_restarts` | cosine_with_restarts调度器的重启次数 | `1` | 正整数 |

### LoRA配置参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `rank` | LoRA更新矩阵的维度 | `16` | 正整数 |
| `lora_layers` | 应用LoRA训练的Transformer模块 | `null` | 逗号分隔的模块名称列表或`null` |
| `freeze_transformer_layers` | 冻结的Transformer层数 | `""` | 逗号分隔的层索引 |

### 数据和验证参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `validation_ratio` | 用于验证的数据集分割比例 | `0.1` | 0-1之间的浮点数 |
| `validation_epochs` | 每X轮运行一次验证 | `1` | 正整数 |
| `caption_dropout` | 标题丢弃比例，用于更新无条件空间 | `0.1` | 0-1之间的浮点数 |
| `mask_dropout` | 掩码丢弃比例，将掩码替换为全0 | `0.05` | 0-1之间的浮点数 |

### 训练控制参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `resume_from_checkpoint` | 从检查点恢复训练 | `null` | 检查点路径或`null` |
| `save_model_epochs` | 每X轮保存一次模型 | `1` | 正整数 |
| `save_model_steps` | 每X步保存一次模型 | `500` | 正整数 |
| `skip_epoch` | 在X轮前跳过验证和模型保存 | `0` | 非负整数 |
| `skip_step` | 在X步前跳过验证和模型保存 | `0` | 非负整数 |
| `save_name` | 检查点的保存名称前缀 | `"flux_fill"` | 任意字符串 |

### 图像训练特定参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `resolution` | 训练的默认分辨率 | `"512"` | `"512"`, `"1024"` |
| `noise_offset` | 初始噪声的偏移量 | `0.01` | 浮点数 |
| `blocks_to_swap` | 建议值为10-20，取决于VRAM | `15` | 整数 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `weighting_scheme` | 权重方案类型 | `"logit_normal"` | `"sigma_sqrt"`, `"logit_normal"`, `"mode"`, `"cosmap"`, `"logit_snr"` |
| `logit_mean` | logit_normal权重方案的均值 | `0.0` | 浮点数 |
| `logit_std` | logit_normal权重方案的标准差 | `1.0` | 浮点数 |
| `mode_scale` | mode权重方案的缩放 | `1.29` | 浮点数 |
| `guidance_scale` | FLUX.1 dev变体的引导缩放因子，默认1以保持蒸馏 | `1.0` | 正浮点数 |
| `reg_ratio` | 作为目标迁移学习的正则化。如果未训练不同目标，则设置为1 | `0.7` | 浮点数 |

### 系统和日志参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `seed` | 可重复训练的随机种子 | `42` | 任意整数 |
| `mixed_precision` | 混合精度训练类型 | `"bf16"` | `"bf16"`, `"fp8"` |
| `logging_dir` | TensorBoard日志目录 | `"logs"` | 任意有效的目录路径 |
| `report_to` | 报告结果和日志的集成平台 | `"wandb"` | `"tensorboard"`, `"wandb"`, `"comet_ml"`, `"all"` |
| `allow_tf32` | 是否允许在Ampere GPU上使用TF32加速训练 | `true` | `true`, `false` |

### 缓存参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `recreate_cache` | 重新创建所有缓存 | `false` | `true`, `false` |

## 配置文件示例

### JSON配置文件示例

```json
{
    "pretrained_model_name_or_path": "black-forest-labs/FLUX.1-dev",
    "repeats": 1,
    "validation_epochs": 1,
    "output_dir": "output/flux-fill",
    "seed": 42,
    "train_batch_size": 1,
    "num_train_epochs": 10,
    "resume_from_checkpoint": null,
    "save_name": "flux_fill",
    "gradient_accumulation_steps": 1,
    "gradient_checkpointing": true,
    "learning_rate": 1e-4,
    "lr_scheduler": "constant",
    "cosine_restarts": 1,
    "lr_warmup_steps": 50,
    "optimizer": "AdamW",
    "logging_dir": "logs",
    "report_to": "wandb",
    "mixed_precision": "bf16",
    "train_data_dir": "data/flux-fill",
    "rank": 32,
    "save_model_epochs": 1,
    "save_model_steps": 500,
    "skip_epoch": 0,
    "skip_step": 0,
    "validation_ratio": 0.1,
    "model_path": null,
    "allow_tf32": true,
    "recreate_cache": false,
    "caption_dropout": 0.1,
    "mask_dropout": 0.05,
    "resolution": "512",
    "weighting_scheme": "logit_normal",
    "logit_mean": 0.0,
    "logit_std": 1.0,
    "mode_scale": 1.29,
    "freeze_transformer_layers": "",
    "lora_layers": null,
    "guidance_scale": 1.0,
    "blocks_to_swap": 15,
    "noise_offset": 0.01,
    "reg_ratio": 0.7,
    "reg_timestep": 900,
    "config_path": "config_flux_fill.json"
}
```

## 训练数据格式要求

### 数据集结构
训练数据目录必须包含以下三种图像文件，文件名需要遵循特定的命名规则：

```
data/flux-fill/
├── image1_G.jpg     # Ground Truth图像（移除对象后的图像）
├── image1_F.jpg     # Factual图像（包含要移除对象的原始图像）
├── image1_M.jpg     # Mask图像（标记要移除对象的掩码图像）
├── image2_G.jpg
├── image2_F.jpg
├── image2_M.jpg
└── ...
```

### 文件命名规则
- **Ground Truth图像**：后缀为 `_G` 的图像文件，表示移除对象后的干净图像
- **Factual图像**：后缀为 `_F` 的图像文件，表示包含要移除对象的原始图像
- **Mask图像**：后缀为 `_M` 的图像文件，表示标记要移除对象的掩码图像

### 文件格式要求
- 图像文件：支持 JPG/JPEG/PNG/WebP 格式
- Mask图像：应为单通道灰度图像，对象区域为白色（255），背景为黑色（0）
- 所有三种图像（G、F、M）必须具有相同的尺寸

### 数据集示例结构
```
data/flux-fill/
├── person/
│   ├── 1_G.jpg
│   ├── 1_F.jpg
│   └── 1_M.jpg
├── animal/
│   ├── 1_G.jpg
│   ├── 1_F.jpg
│   └── 1_M.jpg
└── object/
    ├── 1_G.jpg
    ├── 1_F.jpg
    └── 1_M.jpg
```

## 常见问题

**Q: 如何启动训练？**
A: 使用命令行运行训练脚本，并指定配置文件：
```bash
python train_flux_lora_ui_with_mask.py --config_path=config_flux_fill.json
```

**Q: 训练数据格式要求？**
A: 需要三组图像文件（Ground Truth、Factual、Mask），按照 `_G`、`_F`、`_M` 后缀命名。这些格式是训练脚本硬编码要求的。

**Q: 如何恢复训练？**
A: 使用 `resume_from_checkpoint` 参数从检查点恢复：
```bash
python train_flux_lora_ui_with_mask.py --config_path=config_flux_fill.json --resume_from_checkpoint="latest"
```

**Q: 如何减少显存使用？**
A: 可以通过以下方式减少显存使用：
- 降低 `train_batch_size`（推荐1）
- 启用 `gradient_checkpointing`
- 减少 `rank` 值
- 使用 `blocks_to_swap` 参数进行块交换

**Q: 训练完成后如何使用LoRA权重？**
A: 训练完成后，LoRA权重会保存在指定的输出目录中，可以通过Diffusers库加载使用：

```python
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe.load_lora_weights("./output/flux-fill")
```