# Kolors LoRA 训练参数说明文档

本文档详细介绍了 `train_kolors_lora_ui.py` 训练脚本的所有参数，并说明如何通过UI界面启动训练。

## UI界面

`train_kolors_lora_ui.py` 对应的UI界面是一个基于Web的交互式训练配置界面，通常通过以下方式启动：

### 启动UI界面
```bash
# 直接运行UI启动脚本
python ui_kolors_lora.py
```

### 启动训练脚本
```bash
# 基础训练命令
python train_kolors_lora_ui.py \
    --pretrained_model_name_or_path="Kwai-Kolors/Kolors" \
    --train_data_dir="./datasets/your_images" \
    --output_dir="./output/kolors_lora" \
    --rank=32 \
    --learning_rate=1e-4 \
    --train_batch_size=2 \
    --num_train_epochs=10

# 使用配置文件训练
python train_kolors_lora_ui.py @config.txt
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
| `--train_batch_size` | 训练数据加载器的批次大小（每个设备） | `4` | 正整数 |
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
| `--lr_scheduler` | 要使用的调度器类型 | `constant` | `linear`, `cosine`, `cosine_with_restarts`, `polynomial`, `constant`, `constant_with_warmup` |
| `--lr_warmup_steps` | 学习率调度器的预热步数 | `50` | 非负整数 |
| `--cosine_restarts` | cosine_with_restarts调度器的重启次数 | `1` | 正整数 |

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
| `--validation_epochs` | 每X轮运行一次验证 | `1` | 正整数 |

### 训练控制参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--resume_from_checkpoint` | 从检查点恢复训练 | `None` | 检查点路径或"latest" |
| `--save_model_epochs` | 每X轮保存一次模型 | `1` | 正整数 |
| `--skip_epoch` | 在X轮前跳过验证和模型保存 | `0` | 非负整数 |
| `--skip_step` | 在X步前跳过验证和模型保存 | `0` | 非负整数 |
| `--save_name` | 检查点的保存名称前缀 | `sd3_` | 任意字符串 |

### 高级训练参数

| 参数名 | 参数说明 | 默认值 | 可选值 |
|-----------|-------------|---------------|-----------------|
| `--snr_gamma` | 用于损失再平衡的SNR加权gamma | `5` | 非负浮点数（推荐值：5.0） |
| `--use_debias` | 使用去偏估计损失 | `False` | `True`, `False` |
| `--max_time_steps` | 训练的最大时间步限制 | `1100` | 正整数（0到max_time_steps） |
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
| `--resolution` | 训练的默认分辨率 | `1024` | `1024`, `512` |

## 配置文件示例

创建 `config_kolors.txt` 文件，内容如下：

```text
--pretrained_model_name_or_path=Kwai-Kolors/Kolors
--train_data_dir=./datasets
--output_dir=./output/kolors_lora
--rank=32
--learning_rate=1e-4
--train_batch_size=2
--num_train_epochs=10
--gradient_accumulation_steps=1
--gradient_checkpointing
--mixed_precision=bf16
--save_model_epochs=1
--validation_epochs=1
--save_name=kolors_lora
--validation_ratio=0.1
--caption_dropout=0.1
--optimizer=adamw
--lr_scheduler=constant
--lr_warmup_steps=50
--seed=42
```

### 使用配置文件训练
```bash
python train_kolors_lora_ui.py @config_kolors.txt
```

## 常见问题

**Q: 如何启动训练？**
A: 可以通过UI界面点击"开始训练"按钮，或在命令行使用python train_kolors_lora_ui.py + 参数

**Q: 训练数据格式要求？**
A: 图片格式支持jpg、jpeg、png、webp，每张图片需要有对应的文本描述文件

**Q: 如何恢复训练？**
A: 使用`--resume_from_checkpoint="latest"`参数即可从最新检查点恢复