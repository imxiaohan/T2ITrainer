# Kolors Slider 训练参数说明文档

本文档详细介绍了 `train_kolors_slider.py` 训练脚本的所有参数，这是一个专门用于概念编辑的滑块训练脚本，通过正负样本对来训练LoRA模型。

## 启动训练脚本
```bash
# 基础训练命令
python train_kolors_slider.py \
    --pretrained_model_name_or_path="Kwai-Kolors/Kolors" \
    --train_data_dir="./datasets/slider_images" \
    --output_dir="./output/kolors_slider" \
    --rank=32 \
    --learning_rate=1e-4 \
    --train_batch_size=1 \
    --num_train_epochs=5

# 使用配置文件训练
python train_kolors_slider.py @config_slider.txt
```

## 参数详细说明

### 模型和路径参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--pretrained_model_name_or_path` | 预训练模型路径或HuggingFace模型标识符 | `None` | 任意有效的模型路径或HF模型ID |
| `--output_dir` | 模型预测结果和检查点的输出目录 | `sd3-dreambooth` | 任意有效的目录路径 |
| `--model_path` | 从文件加载模型的独立路径 | `None` | 任意有效的模型文件路径 |
| `--vae_path` | 加载自定义VAE的独立路径 | `None` | 任意有效的VAE文件路径 |

### 训练超参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_batch_size` | 训练数据加载器的批次大小（每个设备） | `1` | 正整数 |
| `--num_train_epochs` | 训练轮数 | `1` | 正整数 |
| `--learning_rate` | 初始学习率（热身期后） | `1e-4` | 正浮点数 |
| `--gradient_accumulation_steps` | 执行反向/更新步骤前累积的更新步数 | `1` | 正整数 |
| `--gradient_checkpointing` | 是否使用梯度检查点以节省内存（牺牲反向传播速度） | `False` | `True`, `False` |
| `--max_grad_norm` | 梯度裁剪的最大范数 | `1.0` | 正浮点数 |
| `--repeats` | 训练数据的重复次数 | `1` | 正整数 |

### 优化器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--optimizer` | 要使用的优化器类型 | `AdamW` | `AdamW`, `prodigy` |
| `--use_8bit_adam` | 是否使用bitsandbytes的8位Adam | `False` | `True`, `False` |
| `--adam_beta1` | Adam和Prodigy优化器的beta1参数 | `0.9` | 0-1之间的浮点数 |
| `--adam_beta2` | Adam和Prodigy优化器的beta2参数 | `0.999` | 0-1之间的浮点数 |
| `--adam_weight_decay` | UNet参数的权重衰减 | `1e-02` | 非负浮点数 |
| `--adam_weight_decay_text_encoder` | 文本编码器的权重衰减 | `1e-03` | 非负浮点数 |
| `--adam_epsilon` | Adam和Prodigy优化器的epsilon值 | `1e-08` | 正浮点数 |

### Prodigy优化器专用参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--prodigy_beta3` | 使用运行平均值计算Prodigy步长的系数 | `None` | 浮点数或None |
| `--prodigy_decouple` | 使用AdamW风格的解耦权重衰减 | `True` | `True`, `False` |
| `--prodigy_use_bias_correction` | 开启Adam的偏差校正 | `True` | `True`, `False` |
| `--prodigy_safeguard_warmup` | 从D估计的分母中移除lr以避免热身阶段问题 | `True` | `True`, `False` |
| `--prodigy_d_coef` | Prodigy的维度系数 | `2` | 正浮点数 |

### 学习率调度器参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--lr_scheduler` | 要使用的调度器类型 | `cosine` | `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup` |
| `--lr_warmup_steps` | 学习率调度器的预热步数 | `50` | 非负整数 |

### LoRA配置参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--rank` | LoRA更新矩阵的维度 | `4` | 正整数 |
| `--use_dora` | 是否使用DoRA（权重分解LoRA） | `False` | `True`, `False` |

### 数据和验证参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--train_data_dir` | 训练数据图像文件夹 | `""` | 任意有效的目录路径 |
| `--validation_ratio` | 用于验证的数据集分割比例 | `0.1` | 0-1之间的浮点数 |
| `--validation_epochs` | 每X轮运行一次验证 | `50` | 正整数 |

### Slider训练专用参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--main_prompt` | 主提示词，用于正负样本的基础描述 | `a girl` | 任意文本 |
| `--pos_prompt` | 正样本提示词，描述想要增强的特征 | `beatiful` | 任意文本 |
| `--neg_prompt` | 负样本提示词，描述想要减弱的特征 | `ugly` | 任意文本 |
| `--steps` | 图像生成步数 | `50` | 正整数 |
| `--cfg` | 图像生成引导比例 | `3.5` | 正浮点数 |
| `--generation_batch` | 图像生成批次大小 | `5` | 正整数 |
| `--image_prefix` | 图像文件名前缀 | `image` | 任意字符串 |

### 训练控制参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resume_from_checkpoint` | 从检查点恢复训练 | `None` | 检查点路径或"latest" |
| `--save_model_epochs` | 每X轮保存一次模型 | `1` | 正整数 |
| `--skip_epoch` | 在X轮前跳过验证和模型保存 | `1` | 非负整数 |
| `--skip_step` | 在X步前跳过验证和模型保存 | `1` | 非负整数 |
| `--break_epoch` | 在X轮后中断训练 | `1` | 正整数 |
| `--save_name` | 检查点的保存名称前缀 | `sd3_` | 任意字符串 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--caption_dropout` | 标题丢弃比例 | `0.1` | 0-1之间的浮点数 |

### 系统和日志参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--seed` | 可重复训练的随机种子 | `None` | 任意整数 |
| `--mixed_precision` | 是否使用混合精度训练 | `None` | `no`, `fp16`, `bf16` |
| `--logging_dir` | TensorBoard日志目录 | `logs` | 任意有效的目录路径 |
| `--report_to` | 报告结果和日志的集成平台 | `wandb` | `tensorboard`, `wandb`, `comet_ml`, `all` |

### 缓存和处理参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--recreate_cache` | 重新创建所有缓存文件 | `False` | `True`, `False` |

## 训练数据格式要求

Slider训练需要特殊的文件夹结构：

```
datasets/
└── slider_images/
    ├── positive/          # 正样本图片
    │   ├── image1.jpg
    │   ├── image2.png
    │   └── ...
    └── negative/          # 负样本图片
        ├── image1.jpg
        ├── image2.png
        └── ...
```

要求：
- 正样本和负样本的图片数量必须相同
- 支持图片格式：jpg、jpeg、png、webp
- 图片文件名应一一对应

## 配置文件示例

创建 `config_slider.txt` 文件，内容如下：

```text
--pretrained_model_name_or_path=Kwai-Kolors/Kolors
--train_data_dir=./datasets/slider_images
--output_dir=./output/kolors_slider
--rank=32
--learning_rate=1e-4
--train_batch_size=1
--num_train_epochs=5
--gradient_accumulation_steps=1
--gradient_checkpointing
--mixed_precision=bf16
--save_model_epochs=1
--validation_epochs=50
--save_name=kolors_slider
--validation_ratio=0.1
--caption_dropout=0.1
--optimizer=adamw
--lr_scheduler=cosine
--lr_warmup_steps=50
--seed=42
--main_prompt="a girl"
--pos_prompt="beautiful"
--neg_prompt="ugly"
--steps=50
--cfg=3.5
--generation_batch=5
--image_prefix="slider"
```

### 使用配置文件训练
```bash
python train_kolors_slider.py @config_slider.txt
```

## Slider训练概念说明

Slider训练是一种特殊的概念编辑技术：

1. **主提示词**：描述图像主体的基础提示词
2. **正提示词**：描述想要增强的特征
3. **负提示词**：描述想要减弱的特征

例如：
- 主提示词：`a girl`
- 正提示词：`beautiful`
- 负提示词：`ugly`

训练完成后，模型可以在这两个概念之间进行平滑过渡。

## 常见问题

**Q: 如何启动Slider训练？**
A: 在命令行使用python train_kolors_slider.py + 参数，或使用配置文件python train_kolors_slider.py @config_slider.txt

**Q: Slider训练数据格式要求？**
A: 需要在训练数据目录下创建positive和negative两个子文件夹，分别放置对应的概念图片

**Q: 如何恢复训练？**
A: 使用`--resume_from_checkpoint="latest"`参数即可从最新检查点恢复

**Q: 正样本和负样本图片数量必须相同吗？**
A: 是的，系统会自动使用最小数量的图片进行配对训练

**Q: 如何调整概念编辑的强度？**
A: 可以通过调整`--steps`（生成步数）和`--cfg`（引导比例）参数来控制编辑效果