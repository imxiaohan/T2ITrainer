# Qwen Image LoRA 训练参数说明文档

本文档详细介绍了 `train_qwen_image.py` 训练脚本的所有参数，用于训练Qwen图像模型的LoRA权重。

## 训练脚本启动

### 基础训练命令
```bash
# 基础训练命令
python train_qwen_image.py \
    --pretrained_model_name_or_path="Qwen/Qwen-Image" \
    --train_data_dir="./datasets/images" \
    --output_dir="./output/qwen_lora" \
    --rank=16 \
    --repeats=10 \
    --resolution=1024 \
    --train_batch_size=1 \
    --num_train_epochs=10 \
    --save_name="qwen_image" \
    --learning_rate=1e-4

# 使用JSON配置文件训练
python train_qwen_image.py --config_path=config_qwen_single.json
```

## 参数详细说明

### 模型和路径参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--pretrained_model_name_or_path` | 预训练模型路径或HuggingFace模型标识符 | `None` | 任意有效的模型路径或HF模型ID |
| `--output_dir` | 模型预测结果和检查点的输出目录 | `flux-dreambooth` | 任意有效的目录路径 |
| `--model_path` | 从文件加载模型的独立路径 | `None` | 任意有效的模型文件路径 |
| `--config_path` | JSON配置文件路径 | `config_qwen_single.json` | 任意有效的配置文件路径 |

### 训练超参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_batch_size` | 训练数据加载器的批次大小（每个设备） | `1` | 正整数 |
| `--num_train_epochs` | 训练轮数 | `10` | 正整数 |
| `--learning_rate` | 初始学习率（热身期后） | `1e-4` | 正浮点数 |
| `--gradient_accumulation_steps` | 执行反向/更新步骤前累积的更新步数 | `1` | 正整数 |
| `--gradient_checkpointing` | 是否使用梯度检查点以节省内存 | `False` | `True`, `False` |
| `--repeats` | 训练数据的重复次数 | `10` | 正整数 |

### 优化器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--optimizer` | 要使用的优化器类型 | `AdamW` | `AdamW`, `prodigy` |

### Prodigy优化器专用参数

| 参数名 | 参数说明 | 默认值 | 可选值 |

### 学习率调度器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--lr_scheduler` | 要使用的调度器类型 | `constant` | `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup` |
| `--lr_warmup_steps` | 学习率调度器的预热步数 | `50` | 非负整数 |
| `--cosine_restarts` | cosine_with_restarts调度器的重启次数 | `1` | 正整数 |

### LoRA配置参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--rank` | LoRA更新矩阵的维度 | `16` | 正整数 |
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
| `--save_name` | 检查点的保存名称前缀 | `qwen_image` | 任意字符串 |

### 图像训练特定参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resolution` | 训练的默认分辨率 | `1024` | `512`, `1024` |
| `--caption_dropout` | 标题丢弃比例 | `0.1` | 0-1之间的浮点数 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--weighting_scheme` | 权重方案类型 | `logit_normal` | `sigma_sqrt`, `logit_normal`, `mode`, `cosmap`, `logit_snr` |
| `--logit_mean` | logit_normal权重方案的均值 | `0.0` | 浮点数 |
| `--logit_std` | logit_normal权重方案的标准差 | `1.0` | 浮点数 |
| `--mode_scale` | mode权重方案的缩放 | `1.29` | 浮点数 |
| `--noise_offset` | 初始噪声的偏移量 | `0.01` | 浮点数 |

### 系统和日志参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--seed` | 可重复训练的随机种子 | `4321` | 任意整数 |
| `--mixed_precision` | 混合精度训练类型 | `None` | `bf16`, `fp8` |
| `--logging_dir` | TensorBoard日志目录 | `logs` | 任意有效的目录路径 |
| `--report_to` | 报告结果和日志的集成平台 | `wandb` | `tensorboard`, `wandb`, `comet_ml`, `all` |
| `--allow_tf32` | 是否允许在Ampere GPU上使用TF32加速训练 | `False` | `True`, `False` |

### 缓存和处理参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--recreate_cache` | 重新创建所有缓存文件 | `False` | `True`, `False` |
| `--blocks_to_swap` | 块交换的块数（根据VRAM设置） | `10` | 10-20之间的整数 |
| `--noise_offset` | 初始噪声的偏移量 | `0.01` | 浮点数 |


## 配置文件示例

### JSON配置文件示例

创建 `config_qwen_single.json` 文件：

```json
{
    "pretrained_model_name_or_path": "F:\\T2ITrainer\\qwen_models\\qwen_image_nf4",
    "output_dir": "F:\\models\\qwen\\kontext_single",
    "train_data_dir": "F:\\ImageSet\\aigate_demo\\kontext_single",
    "save_name": "highres_test",
    "repeats": 10,
    "validation_epochs": 1,
    "seed": 4321,
    "train_batch_size": 1,
    "num_train_epochs": 10,
    "resume_from_checkpoint": "",
    "gradient_accumulation_steps": 1,
    "gradient_checkpointing": true,
    "learning_rate": 0.0001,
    "lr_scheduler": "cosine",
    "cosine_restarts": 1,
    "lr_warmup_steps": 50,
    "optimizer": "adamw",
    "logging_dir": "logs",
    "report_to": "wandb",
    "mixed_precision": "bf16",
    "rank": 32,
    "save_model_epochs": 1,
    "save_model_steps": -1,
    "skip_epoch": 0,
    "skip_step": 0,
    "validation_ratio": 0.1,
    "allow_tf32": true,
    "recreate_cache": true,
    "caption_dropout": 0.1,
    "resolution": "512",
    "weighting_scheme": "logit_normal",
    "logit_mean": 0.0,
    "logit_std": 1.0,
    "mode_scale": 1.29,
    "freeze_transformer_layers": "",
    "lora_layers": "",
    "blocks_to_swap": 10,
    "noise_offset": 0.01,
    "model_path": "",
    "image_configs": {
        "train": {
            "suffix": ""
        }
    },
    "caption_configs": {
        "train": {
            "ext": ".txt"
        }
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

### 使用配置文件训练

```bash
# 使用JSON配置文件（支持）
python train_qwen_image.py --config_path=config_qwen_single.json
```

## 训练数据格式要求

### 数据结构
训练数据目录应包含以下文件：

```
datasets/
└── images/
    ├── image1.jpg          # 训练图像
    ├── image1.txt          # 图像的描述
    ├── image2.jpg
    ├── image2.txt
    └── ...
```

### 文件命名规则
- 图像文件：任意有效的图像文件名
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
                }
            },
            "captions_selection": {
                "target": "train"
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
        "train": {"suffix": ""}
    }
}
```

**3. caption_configs**
定义描述文件扩展名：

```json
{
    "caption_configs": {
        "train": {"ext": ".txt"}
    }
}
```

### 实际配置示例

**单图像训练配置：**
```json
{
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
    ],
    "image_configs": {
        "train": {"suffix": ""}
    },
    "caption_configs": {
        "train": {"ext": ".txt"}
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
python train_qwen_image.py --config_path=config_qwen_single.json
```

**Q: 训练数据格式要求？**
A: 需要图像文件和对应的文本描述文件，格式为 `.txt`。

**Q: 如何恢复训练？**
A: 使用 `--resume_from_checkpoint="latest"` 参数从最新检查点恢复：
```bash
python train_qwen_image.py --resume_from_checkpoint="latest" --config_path=config_qwen_single.json
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
from diffusers import QwenImagePipeline

pipe = QwenImagePipeline.from_pretrained(
    "Qwen/Qwen-Image",
    torch_dtype=torch.float16
)
pipe.load_lora_weights("./output/qwen_lora")
```
