# Flux Kontext LoRA 训练参数说明文档（新版）

本文档详细介绍了 `train_flux_lora_ui_kontext_new.py` 训练脚本的所有参数，用于训练Flux Kontext模型的LoRA权重。

## 训练脚本启动

### 基础训练命令
```bash
# 基础训练命令
python train_flux_lora_ui_kontext_new.py \
    --pretrained_model_name_or_path="black-forest-labs/FLUX.1-dev" \
    --train_data_dir="./datasets/flux_training" \
    --output_dir="./output/flux_kontext_lora" \
    --rank=32 \
    --learning_rate=1e-4 \
    --train_batch_size=1 \
    --num_train_epochs=10

# 使用JSON配置文件训练
python train_flux_lora_ui_kontext_new.py --config_path=config_new_pairs.json
```

## 参数详细说明

### 模型和路径参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--pretrained_model_name_or_path` | 预训练模型路径或HuggingFace模型标识符 | `None` | 任意有效的模型路径或HF模型ID |
| `--output_dir` | 模型预测结果和检查点的输出目录 | `flux-dreambooth` | 任意有效的目录路径 |
| `--model_path` | 从文件加载模型的独立路径 | `None` | 任意有效的模型文件路径 |

### 训练超参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_batch_size` | 训练数据加载器的批次大小（每个设备） | `1` | 正整数 |
| `--num_train_epochs` | 训练轮数 | `1` | 正整数 |
| `--learning_rate` | 初始学习率（热身期后） | `1e-4` | 正浮点数 |
| `--gradient_accumulation_steps` | 执行反向/更新步骤前累积的更新步数 | `1` | 正整数 |
| `--gradient_checkpointing` | 是否使用梯度检查点以节省内存 | `False` | `True`, `False` |
| `--repeats` | 训练数据的重复次数 | `1` | 正整数 |

### 优化器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--optimizer` | 要使用的优化器类型 | `AdamW` | `AdamW`, `prodigy` |

### 学习率调度器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--lr_scheduler` | 要使用的调度器类型 | `constant` | `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup` |
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

### 图像处理参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resolution` | 训练的默认分辨率 | `512` | `512`, `1024` |
| `--caption_dropout` | 标题丢弃比例 | `0.1` | 0-1之间的浮点数 |
| `--noise_offset` | 初始噪声中的噪声偏移 | `0.01` | 浮点数 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--weighting_scheme` | 权重方案类型 | `logit_normal` | `sigma_sqrt`, `logit_normal`, `mode`, `cosmap`, `logit_snr` |
| `--logit_mean` | logit_normal权重方案的均值 | `0.0` | 浮点数 |
| `--logit_std` | logit_normal权重方案的标准差 | `1.0` | 浮点数 |
| `--mode_scale` | mode权重方案的缩放 | `1.29` | 浮点数 |

### 系统和日志参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--seed` | 可重复训练的随机种子 | `42` | 任意整数 |
| `--mixed_precision` | 混合精度训练类型 | `bf16` | `bf16`, `fp8` |
| `--logging_dir` | TensorBoard日志目录 | `logs` | 任意有效的目录路径 |
| `--report_to` | 报告结果和日志的集成平台 | `wandb` | `tensorboard`, `wandb`, `comet_ml`, `all` |
| `--allow_tf32` | 是否允许在Ampere GPU上使用TF32加速训练 | `False` | `True`, `False` |

### 缓存和处理参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--recreate_cache` | 重新创建所有缓存文件 | `False` | `True`, `False` |
| `--blocks_to_swap` | 块交换的块数（根据VRAM设置） | `10` | 10-20之间的整数 |

### 配置参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--config_path` | 配置文件路径 | `config.json` | 任意有效的JSON文件路径 |

## 配置文件示例

### 1. 单图训练配置 (config_new_single.json)
适用于单图像训练任务：

```json
{
    "pretrained_model_name_or_path": "F:\\T2ITrainer\\flux_models\\kontext",
    "output_dir": "F:\\models\\flux\\training_demo",
    "save_name": "training_demo",
    "train_data_dir": "F:\\ImageSet\\tryon\\demo_dataset_single",
    "repeats": 10,
    "validation_epochs": 1,
    "seed": 4321,
    "train_batch_size": 1,
    "num_train_epochs": 10,
    "gradient_accumulation_steps": 1,
    "gradient_checkpointing": true,
    "learning_rate": 0.0001,
    "lr_scheduler": "constant",
    "cosine_restarts": 1,
    "lr_warmup_steps": 0,
    "optimizer": "adamw",
    "mixed_precision": "bf16",
    "rank": 32,
    "save_model_epochs": 1,
    "save_model_steps": -1,
    "validation_ratio": 0.1,
    "caption_dropout": 0.1,
    "resolution": "512",
    "weighting_scheme": "logit_normal",
    "logit_mean": 0.0,
    "logit_std": 1.0,
    "mode_scale": 1.29,
    "guidance_scale": 1,
    "image_configs": {
        "train": {"suffix": ""}
    },
    "caption_configs": {
        "train": {"ext": ".txt"}
    },
    "training_set": [
        {
            "training_layout_configs": {
                "train": {
                    "target": "train",
                    "noised": true
                }
            },
            "captions_selection": {
                "target": "train"
            }
        }
    ]
}
```

### 2. 双图对训练配置 (config_new_pairs.json)
适用于目标图像+参考图像的成对训练：

```json
{
    "pretrained_model_name_or_path": "F:\\T2ITrainer\\flux_models\\kontext",
    "output_dir": "F:\\models\\flux\\training_demo",
    "save_name": "training_demo",
    "train_data_dir": "F:\\ImageSet\\tryon\\demo_dataset",
    "repeats": 10,
    "validation_epochs": 1,
    "seed": 4321,
    "train_batch_size": 1,
    "num_train_epochs": 10,
    "gradient_accumulation_steps": 1,
    "gradient_checkpointing": true,
    "learning_rate": 0.0001,
    "lr_scheduler": "constant",
    "cosine_restarts": 1,
    "lr_warmup_steps": 0,
    "optimizer": "adamw",
    "mixed_precision": "bf16",
    "rank": 32,
    "save_model_epochs": 1,
    "save_model_steps": -1,
    "validation_ratio": 0.1,
    "caption_dropout": 0.1,
    "resolution": "512",
    "weighting_scheme": "logit_normal",
    "logit_mean": 0.0,
    "logit_std": 1.0,
    "mode_scale": 1.29,
    "guidance_scale": 1,
    "image_configs": {
        "train": {"suffix": "_T"},
        "reference": {"suffix": "_R"}
    },
    "caption_configs": {
        "train": {"ext": ".txt"}
    },
    "training_set": [
        {
            "training_layout_configs": {
                "train": {
                    "target": "train",
                    "noised": true
                },
                "reference": {
                    "target": "reference"
                }
            },
            "captions_selection": {
                "target": "train"
            }
        }
    ]
}
```

### 3. 多图对训练配置 (config_new_pairs_multiple.json)
适用于包含额外参考图像的多图训练：

```json
{
    "pretrained_model_name_or_path": "F:\\T2ITrainer\\flux_models\\kontext",
    "output_dir": "F:\\models\\flux\\multiple_training_demo",
    "save_name": "multiple_training_demo",
    "train_data_dir": "F:\\ImageSet\\tryon\\demo_dataset",
    "repeats": 10,
    "image_configs": {
        "train": {"suffix": "_T"},
        "reference": {"suffix": "_R"},
        "grey": {"suffix": "_G"}
    },
    "caption_configs": {
        "train": {"ext": ".txt"}
    },
    "training_set": [
        {
            "training_layout_configs": {
                "train": {
                    "target": "train",
                    "noised": true
                },
                "reference": {
                    "target": "reference"
                },
                "grey": {
                    "target": "grey",
                    "dropout": 0.5
                }
            },
            "captions_selection": {
                "target": "train"
            }
        }
    ]
}
```

### 4. 混合训练配置 (config_new_mixed.json)
适用于同时训练对图和单图的混合模式：

```json
{
    "pretrained_model_name_or_path": "F:\\T2ITrainer\\flux_models\\kontext",
    "output_dir": "F:\\models\\flux\\training_demo",
    "save_name": "training_demo",
    "train_data_dir": "F:\\ImageSet\\0outsource\\digital human\\3d_human_test",
    "repeats": 10,
    "image_configs": {
        "train": {"suffix": "_T"},
        "reference": {"suffix": "_R"},
        "train_single": {"suffix": "_T"}
    },
    "caption_configs": {
        "train": {"ext": ".txt"},
        "train_single": {"ext": "1.txt"}
    },
    "training_set": [
        {
            "training_layout_configs": {
                "train": {"target": "train", "noised": true},
                "reference": {"target": "reference"}
            },
            "captions_selection": {"target": "train"},
            "weight": 0.5
        },
        {
            "training_layout_configs": {
                "train_single": {"target": "train_single", "noised": true}
            },
            "captions_selection": {"target": "train_single"},
            "weight": 0.5
        }
    ]
}
```

### 使用配置文件训练

```bash
# 使用JSON配置文件
python train_flux_lora_ui_kontext_new.py --config_path=config_new_pairs.json

# 使用单图训练配置
python train_flux_lora_ui_kontext_new.py --config_path=config_new_single.json

# 使用多图训练配置
python train_flux_lora_ui_kontext_new.py --config_path=config_new_pairs_multiple.json

# 使用混合训练配置
python train_flux_lora_ui_kontext_new.py --config_path=config_new_mixed.json

# 从检查点恢复训练
python train_flux_lora_ui_kontext_new.py --resume_from_checkpoint="latest" --config_path=config_new_pairs.json
```

## 训练数据格式要求

### 数据结构

训练数据目录应包含以下文件：

```
datasets/
└── flux_training/
    ├── image1_T.jpg      # 目标图像
    ├── image1_T.txt      # 目标图像的描述
    ├── image1_R.jpg      # 参考图像
    ├── image1_R.txt      # 参考图像的描述
    ├── image2_T.jpg
    ├── image2_T.txt
    ├── image2_R.jpg
    └── image2_R.txt
```

### 文件命名规则

- `_T` 后缀：目标图像（训练目标）
- `_R` 后缀：参考图像（条件输入）
- 描述文件：与图像文件同名，扩展名为 `.txt`

### 支持的图像格式

- JPG/JPEG
- PNG
- WebP

## 配置结构说明

训练配置通过JSON文件定义，必须包含以下结构：

### 必需的配置项

**1. training_set数组**
定义训练布局，包含`training_layout_configs`和`captions_selection`：

```json
{
    "training_set": [
        {
            "training_layout_configs": {
                "train": {
                    "target": "train",
                    "noised": true
                },
                "reference": {
                    "target": "reference"
                }
            },
            "captions_selection": {
                "target": "reference"
            }
        }
    ]
}
```

**2. image_configs**
定义图像文件的后缀匹配规则：

```json
{
    "image_configs": {
        "train": {"suffix": "_T"},
        "reference": {"suffix": "_R"}
    }
}
```

**3. caption_configs**
定义描述文件扩展名：

```json
{
    "caption_configs": {
        "reference": {"ext": ".txt"}
    }
}
```

### 实际配置示例

**Flux Kontext训练配置：**

```json
{
    "training_set": [
        {
            "training_layout_configs": {
                "train": {
                    "target": "train",
                    "noised": true
                },
                "reference": {
                    "target": "reference"
                }
            },
            "captions_selection": {
                "target": "reference"
            }
        }
    ],
    "image_configs": {
        "train": {"suffix": "_T"},
        "reference": {"suffix": "_R"}
    },
    "caption_configs": {
        "reference": {"ext": ".txt"}
    }
}
```

### 配置说明

- `training_set`必须是数组，包含一个或多个训练配置
- `training_layout_configs`定义哪些图像参与训练及其角色
- `captions_selection`指定使用哪个图像的描述文本
- 系统只使用配置文件中的具体设置，没有预定义的"训练类型"

## 常见问题

**Q: 如何启动训练？**
A: 使用命令行运行训练脚本，可以指定参数或使用配置文件：
```bash
python train_flux_lora_ui_kontext_new.py --config_path=config.json
```

**Q: 训练数据格式要求？**
A: 需要成对的图像（目标图像和参考图像），每张图像需要对应的文本描述文件，格式为 `.txt`。

**Q: 如何减少显存使用？**
A: 可以通过以下方式减少显存使用：
- 降低 `--train_batch_size`（推荐1-2）
- 启用 `--gradient_checkpointing`
- 减少 `--rank` 值
- 使用 `--blocks_to_swap` 参数进行块交换
- 使用 `--mixed_precision bf16`

**Q: 如何恢复训练？**
A: 使用 `--resume_from_checkpoint="latest"` 参数从最新检查点恢复：
```bash
python train_flux_lora_ui_kontext_new.py --resume_from_checkpoint="latest" --config_path=config.json
```

**Q: 训练完成后如何使用LoRA权重？**
A: 训练完成后，LoRA权重会保存在指定的输出目录中，可以通过Diffusers库加载使用：

```python
from flux.pipeline_flux_kontext import FluxKontextPipeline

pipe = FluxKontextPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe.load_lora_weights("./output/flux_kontext_lora")
```