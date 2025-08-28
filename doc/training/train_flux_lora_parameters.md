# Flux LoRA 训练参数说明文档

本文档详细介绍了 `train_flux_lora_ui_kontext.py` 训练脚本的所有参数，用于训练Flux模型的LoRA权重。

## 训练脚本启动

### 基础训练命令
```bash
# 基础训练命令
python train_flux_lora_ui_kontext.py \
    --pretrained_model_name_or_path="black-forest-labs/FLUX.1-dev" \
    --train_data_dir="./train_data" \
    --output_dir="./output/flux-lora" \
    --rank=16 \
    --learning_rate=1e-4 \
    --train_batch_size=1 \
    --num_train_epochs=10

# 使用JSON配置文件训练
python train_flux_lora_ui_kontext.py --config_path=config_flux.json
```

## 参数详细说明

### 模型和路径参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--pretrained_model_name_or_path` | 预训练模型路径或HuggingFace模型标识符 | `None` | 任意有效的模型路径或HF模型ID |
| `--output_dir` | 模型预测结果和检查点的输出目录 | `flux-dreambooth` | 任意有效的目录路径 |
| `--model_path` | 从文件加载模型的独立路径 | `None` | 任意有效的模型文件路径 |
| `--vae_path` | 加载自定义VAE的独立路径 | `None` | 任意有效的VAE文件路径 |
| `--config_path` | JSON配置文件路径 | `config.json` | 任意有效的配置文件路径 |

### 训练超参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_batch_size` | 训练数据加载器的批次大小（每个设备） | `1` | 正整数 |
| `--num_train_epochs` | 训练轮数 | `1` | 正整数 |
| `--learning_rate` | 初始学习率（热身期后） | `1e-4` | 正浮点数 |
| `--gradient_accumulation_steps` | 执行反向/更新步骤前累积的更新步数 | `1` | 正整数 |
| `--gradient_checkpointing` | 是否使用梯度检查点以节省内存 | `False` | `True`, `False` |
| `--max_grad_norm` | 梯度裁剪的最大范数 | `1.0` | 正浮点数 |
| `--repeats` | 训练数据的重复次数 | `1` | 正整数 |

### 优化器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--optimizer` | 要使用的优化器类型 | `AdamW` | `AdamW`, `prodigy` |

### 学习率调度器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--lr_scheduler` | 要使用的调度器类型 | `cosine` | `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup` |
| `--lr_warmup_steps` | 学习率调度器的预热步数 | `50` | 非负整数 |
| `--cosine_restarts` | cosine_with_restarts调度器的重启次数 | `1` | 正整数 |

### LoRA配置参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--rank` | LoRA更新矩阵的维度 | `4` | 正整数 |
| `--lora_layers` | 应用LoRA训练的Transformer模块 | `None` | 逗号分隔的模块名称列表 |
| `--freeze_transformer_layers` | 冻结的Transformer层数 | `""` | 逗号分隔的层索引 |

### 数据和验证参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_data_dir` | 训练数据图像文件夹 | `""` | 任意有效的目录路径 |
| `--validation_ratio` | 用于验证的数据集分割比例 | `0.1` | 0-1之间的浮点数 |
| `--validation_epochs` | 每X轮运行一次验证 | `1` | 正整数 |

### 训练控制参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resume_from_checkpoint` | 从检查点恢复训练 | `None` | 检查点路径或"latest" |
| `--save_model_epochs` | 每X轮保存一次模型 | `1` | 正整数 |
| `--save_model_steps` | 每X步保存一次模型 | `-1` | 正整数 |
| `--skip_epoch` | 在X轮前跳过验证和模型保存 | `0` | 非负整数 |
| `--skip_step` | 在X步前跳过验证和模型保存 | `0` | 非负整数 |
| `--save_name` | 检查点的保存名称前缀 | `flux_` | 任意字符串 |

### 图像训练特定参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resolution` | 训练的默认分辨率 | `512` | `512`, `1024` |
| `--caption_dropout` | 标题丢弃比例 | `0.1` | 0-1之间的浮点数 |
| `--mask_dropout` | 掩码丢弃比例 | `0.01` | 0-1之间的浮点数 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--snr_gamma` | 用于损失再平衡的SNR加权gamma | `5` | 非负浮点数（推荐值：5.0） |
| `--max_time_steps` | 训练的最大时间步限制 | `1000` | 正整数（0到max_time_steps） |
| `--weighting_scheme` | 权重方案类型 | `logit_normal` | `sigma_sqrt`, `logit_normal`, `mode`, `cosmap`, `logit_snr` |
| `--logit_mean` | logit_normal权重方案的均值 | `0.0` | 浮点数 |
| `--logit_std` | logit_normal权重方案的标准差 | `1.0` | 浮点数 |
| `--mode_scale` | mode权重方案的缩放 | `1.29` | 浮点数 |
| `--guidance_scale` | 引导缩放因子 | `1` | 正浮点数 |
| `--noise_offset` | 初始噪声的偏移量 | `0.01` | 浮点数 |
| `--reg_ratio` | 目标迁移学习的正则化 | `0.0` | 浮点数 |
| `--reg_timestep` | 目标迁移学习的正则化时间步 | `0` | 整数 |

### 系统和日志参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--seed` | 可重复训练的随机种子 | `42` | 任意整数 |
| `--mixed_precision` | 混合精度训练类型 | `None` | `bf16`, `fp8` |
| `--logging_dir` | TensorBoard日志目录 | `logs` | 任意有效的目录路径 |
| `--report_to` | 报告结果和日志的集成平台 | `wandb` | `tensorboard`, `wandb`, `comet_ml`, `all` |
| `--allow_tf32` | 是否允许在Ampere GPU上使用TF32加速训练 | `False` | `True`, `False` |

### 缓存和处理参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--recreate_cache` | 重新创建所有缓存文件 | `False` | `True`, `False` |
| `--blocks_to_swap` | 块交换的块数（根据VRAM设置） | `10` | 10-20之间的整数 |


## 配置文件示例

### JSON配置文件示例

创建 `config_flux.json` 文件：

```json
{
    "pretrained_model_name_or_path": "black-forest-labs/FLUX.1-dev",
    "output_dir": "./output/flux-lora",
    "save_name": "flux_lora_model",
    "train_data_dir": "./train_data",
    "repeats": 1,
    "validation_epochs": 1,
    "seed": 42,
    "train_batch_size": 1,
    "num_train_epochs": 10,
    "resume_from_checkpoint": "",
    "gradient_accumulation_steps": 4,
    "gradient_checkpointing": true,
    "learning_rate": 1e-4,
    "lr_scheduler": "cosine",
    "cosine_restarts": 1,
    "lr_warmup_steps": 50,
    "optimizer": "AdamW",
    "report_to": "wandb",
    "mixed_precision": "bf16",
    "rank": 16,
    "save_model_epochs": 5,
    "skip_epoch": 0,
    "skip_step": 0,
    "validation_ratio": 0.1,
    "model_path": "",
    "allow_tf32": true,
    "recreate_cache": false,
    "caption_dropout": 0.1,
    "mask_dropout": 0.01,
    "resolution": "512",
    "snr_gamma": 5.0,
    "max_time_steps": 1100,
    "weighting_scheme": "logit_normal",
    "logit_mean": 0.0,
    "logit_std": 1.0,
    "mode_scale": 1.29,
    "freeze_transformer_layers": "",
    "lora_layers": null,
    "guidance_scale": 3.5,
    "blocks_to_swap": 10,
    "noise_offset": 0.01,
    "reg_ratio": 1.0
}
```

### 使用配置文件训练

```bash
# 使用JSON配置文件
python train_flux_lora_ui_kontext.py --config_path=config_flux.json
```

## 训练数据格式要求

### 数据结构
训练数据目录应包含以下文件：

```
train_data/
├── image1.jpg
├── image1.txt
├── image2.jpg
└── image2.txt
```

### 文件命名规则
- 图像文件：支持 JPG/JPEG/PNG/WebP 格式
- 描述文件：与图像文件同名，扩展名为 `.txt`

### 支持的图像格式
- JPG/JPEG
- PNG
- WebP

## 常见问题

**Q: 如何启动训练？**
A: 使用命令行运行训练脚本，可以指定参数或使用配置文件：
```bash
python train_flux_lora_ui_kontext.py --config_path=config_flux.json
```

**Q: 训练数据格式要求？**
A: 需要图像文件和对应的文本描述文件，格式为 `.txt`。这些格式是硬编码的，无法通过配置修改。

**Q: 如何恢复训练？**
A: 使用 `--resume_from_checkpoint="latest"` 参数从最新检查点恢复：
```bash
python train_flux_lora_ui_kontext.py --resume_from_checkpoint="latest" --config_path=config_flux.json
```

**Q: 如何减少显存使用？**
A: 可以通过以下方式减少显存使用：
- 降低 `--train_batch_size`（推荐1-2）
- 启用 `--gradient_checkpointing`
- 减少 `--rank` 值
- 使用 `--blocks_to_swap` 参数进行块交换

**Q: 训练完成后如何使用LoRA权重？**
A: 训练完成后，LoRA权重会保存在指定的输出目录中，可以通过Diffusers库加载使用：

```python
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe.load_lora_weights("./output/flux-lora")
```