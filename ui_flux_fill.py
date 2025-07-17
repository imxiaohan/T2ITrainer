import gradio as gr

import subprocess
import json
import sys
import os

css_code = """
.my-file-upload {
    height: 60px !important;
}
.my-file-upload .download-link {
    display: none !important;
}
.spacing-section {
    margin-bottom: 20px !important;
    padding-bottom: 20px !important;
    border-bottom: 2px dotted #e0e0e0 !important;
}
/* 设置页面整体宽度 */
.gradio-container {
    max-width: 960px !important;
    width: 100% !important;
    margin: 0 auto !important;
}
"""

# ===== 语言翻译系统 =====
# 翻译字典 - 包含所有需要翻译的文本
TRANSLATIONS = {
    'zh': {
        'title': '## LoRA 训练',
        'script': '训练脚本',
        'config_path': '配置文件路径 (.json文件)',
        'config_path_placeholder': '输入保存/加载配置的路径',
        'save': '下载配置',
        'load': '加载配置',
        'directory_section': '目录配置',
        'output_dir': '输出目录',
        'output_dir_placeholder': '检查点保存位置',
        'save_name': '保存名称',
        'save_name_placeholder': '检查点保存名称',
        'pretrained_model_name_or_path': '预训练模型名称或路径',
        'pretrained_model_placeholder': '仓库名称或包含diffusers模型结构的目录',
        'resume_from_checkpoint': '从检查点恢复',
        'resume_checkpoint_placeholder': '从选定目录恢复lora权重',
        'train_data_dir': '训练数据目录',
        'train_data_dir_placeholder': '包含数据集的目录',
        'model_path': '模型路径',
        'model_path_placeholder': '如果不是从官方权重训练则为单个权重文件',
        'report_to': '报告到',
        'lora_config': 'LoRA 配置',
        'rank': '秩',
        'rank_info': '建议对小于100的训练集使用秩4',
        'train_batch_size': '训练批次大小',
        'batch_size_info': '批次大小1使用18GB。请使用小批次大小以避免内存不足',
        'repeats': '重复次数',
        'gradient_accumulation_steps': '梯度累积步数',
        'mixed_precision': '混合精度',
        'gradient_checkpointing': '梯度检查点',
        'optimizer': '优化器',
        'lr_scheduler': '学习率调度器',
        'cosine_restarts': '余弦重启',
        'cosine_restarts_info': '仅对学习率调度器cosine_with_restarts有用',
        'learning_rate': '学习率',
        'learning_rate_info': '推荐：1e-4 或 prodigy使用1',
        'lr_warmup_steps': '学习率预热步数',
        'seed': '随机种子',
        'blocks_to_swap': '交换块数',
        'blocks_to_swap_info': '交换到CPU的块数。建议24GB使用10，更低显存使用更多',
        'mask_dropout': '掩码丢弃',
        'mask_dropout_info': '丢弃掩码，意味着整个图像重建的掩码全为1',
        'reg_ratio': '正则化比率',
        'reg_ratio_info': '作为目标迁移学习的正则化。如果不训练不同目标则设为1',
        'reg_timestep': '正则化时间步',
        'reg_timestep_info': '作为目标迁移学习的正则化。如果不训练不同目标则设为0',
        'misc': '杂项',
        'num_train_epochs': '训练轮数',
        'num_train_epochs_info': '训练的总轮数',
        'save_model_epochs': '保存模型轮数',
        'save_model_epochs_info': '每x轮保存检查点',
        'validation_epochs': '验证轮数',
        'validation_epochs_info': '每x轮执行验证',
        'skip_epoch': '跳过轮数',
        'skip_epoch_info': '跳过x轮进行验证和保存检查点',
        'skip_step': '跳过步数',
        'skip_step_info': '跳过x步进行验证和保存检查点',
        'validation_ratio': '验证比例',
        'validation_ratio_info': '按此比例分割数据集用于验证',
        'recreate_cache': '重新创建缓存',
        'caption_dropout': '标题丢弃',
        'caption_dropout_info': '标题丢弃',
        'max_time_steps': '最大时间步限制',
        'max_time_steps_info': '最大时间步限制',
        'resolution_section': '## 实验选项：分辨率\n- 基于目标分辨率（默认：1024）。\n- 支持512或1024。',
        'resolution': '分辨率',
        'output_box': '输出框',
        'run': '运行',
        'run_button': '运行',
        'language_toggle': '🌐 切换到English',
        'refresh': '刷新',
        'upload_config_file': '上传配置文件',
        'config_file_path': '配置文件路径',
        'download_link': '下载链接',
    },
    'en': {
        'title': '## Lora Training',
        'script': 'script',
        'config_path': 'Config Path (.json file)',
        'config_path_placeholder': 'Enter path to save/load config',
        'save': 'Download Config',
        'load': 'Load Config',
        'directory_section': 'Directory section',
        'output_dir': 'output_dir',
        'output_dir_placeholder': 'checkpoint save to',
        'save_name': 'save_name',
        'save_name_placeholder': 'checkpoint save name',
        'pretrained_model_name_or_path': 'pretrained_model_name_or_path',
        'pretrained_model_placeholder': 'repo name or dir contains diffusers model structure',
        'resume_from_checkpoint': 'resume_from_checkpoint',
        'resume_checkpoint_placeholder': 'resume the lora weight from seleted dir',
        'train_data_dir': 'train_data_dir',
        'train_data_dir_placeholder': 'dir contains dataset',
        'model_path': 'model_path',
        'model_path_placeholder': 'single weight files if not trained from official weight',
        'report_to': 'report_to',
        'lora_config': 'Lora Config',
        'rank': 'rank',
        'rank_info': 'Recommanded to use rank 4 for training set small than 100.',
        'train_batch_size': 'train_batch_size',
        'batch_size_info': 'Batch size 1 is using 18GB. Please use small batch size to avoid oom.',
        'repeats': 'repeats',
        'gradient_accumulation_steps': 'gradient_accumulation_steps',
        'mixed_precision': 'mixed_precision',
        'gradient_checkpointing': 'gradient_checkpointing',
        'optimizer': 'optimizer',
        'lr_scheduler': 'lr_scheduler',
        'cosine_restarts': 'cosine_restarts',
        'cosine_restarts_info': 'Only useful for lr_scheduler: cosine_with_restarts',
        'learning_rate': 'learning_rate',
        'learning_rate_info': 'Recommended: 1e-4 or 1 for prodigy',
        'lr_warmup_steps': 'lr_warmup_steps',
        'seed': 'seed',
        'blocks_to_swap': 'blocks_to_swap',
        'blocks_to_swap_info': 'How many blocks to swap to cpu. It is suggested 10 for 24 GB and more for lower VRAM',
        'mask_dropout': 'mask_dropout',
        'mask_dropout_info': 'Dropout mask which means mask is all one for whole image reconstruction',
        'reg_ratio': 'reg_ratio',
        'reg_ratio_info': 'As regularization of objective transfer learning. Set as 1 if you aren\'t training different objective.',
        'reg_timestep': 'reg_timestep',
        'reg_timestep_info': 'As regularization of objective transfer learning. Set as 0 if you aren\'t training different objective.',
        'misc': 'Misc',
        'num_train_epochs': 'num_train_epochs',
        'num_train_epochs_info': 'Total epoches of the training',
        'save_model_epochs': 'save_model_epochs',
        'save_model_epochs_info': 'Save checkpoint when x epoches',
        'validation_epochs': 'validation_epochs',
        'validation_epochs_info': 'perform validation when x epoches',
        'skip_epoch': 'skip_epoch',
        'skip_epoch_info': 'Skip x epoches for validation and save checkpoint',
        'skip_step': 'skip_step',
        'skip_step_info': 'Skip x steps for validation and save checkpoint',
        'validation_ratio': 'validation_ratio',
        'validation_ratio_info': 'Split dataset with this ratio for validation',
        'recreate_cache': 'recreate_cache',
        'caption_dropout': 'Caption Dropout',
        'caption_dropout_info': 'Caption Dropout',
        'max_time_steps': 'Max timesteps limitation',
        'max_time_steps_info': 'Max timesteps limitation',
        'resolution_section': '## Experiment Option: resolution\n- Based target resolution (default:1024). \n- 512 or 1024 are supported.',
        'resolution': 'resolution',
        'output_box': 'Output Box',
        'run': 'Run',
        'run_button': 'Run',
        'language_toggle': '🌐 切换到中文',
        'refresh': 'Refresh',
        'upload_config_file': 'Upload Config File',
        'config_file_path': 'Config File Path',
        'download_link': 'Download Link',
    }
}

# 当前语言状态
current_language = 'en'

# 从配置文件加载默认配置
def load_default_config():
    """从default_config.json加载默认配置"""
    try:
        with open("default_config.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading default config: {e}")
        # 如果加载失败，返回空配置
        return {
            "script": "train_flux_lora_ui_kontext.py",
            "script_choices": [
                "train_flux_lora_ui_kontext.py",
                "train_flux_lora_ui_with_mask.py",
                "train_flux_lora_ui.py"
            ],
            "config_path": "default_config.json"
        }

# 加载默认配置
default_config = load_default_config()



# 页面初始化配置 - 使用默认配置
page_config = default_config

# 获取当前语言的文本
def get_text(key):
    """获取当前语言的文本"""
    return TRANSLATIONS[current_language].get(key, key)

def toggle_language():
    """切换语言"""
    global current_language
    current_language = 'en' if current_language == 'zh' else 'zh'
    return current_language

# 保存配置
def save_config( 
        config_path,
        script,
        seed,
        # logging_dir,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        # break_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        # use_dora,
        recreate_cache,
        # vae_path,
        resolution,
        # use_debias,
        # snr_gamma,
        caption_dropout,
        cosine_restarts,
        max_time_steps,
        blocks_to_swap,
        mask_dropout,
        reg_ratio,
        reg_timestep
        # use_fp8
        # freeze_transformer_layers
    ):
    # Ensure config_path is just filename, save to configs directory
    configs_dir = os.path.join(os.getcwd(), "configs")
    os.makedirs(configs_dir, exist_ok=True)
    
    # Handle config_path which might be a relative path
    if config_path:
        # If config_path contains directory separators, it's a relative path
        if '/' in config_path or '\\' in config_path:
            # Use the relative path as is
            filename = config_path
        else:
            # If just filename provided
            filename = config_path
    else:
        filename = "config.json"
    
    # Ensure .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Create full path in configs directory
    full_config_path = os.path.join(configs_dir, filename)
    
    config = {
        "script":script,
        "seed":seed,
        # "logging_dir":logging_dir,
        "mixed_precision":mixed_precision,
        "report_to":report_to,
        "lr_warmup_steps":lr_warmup_steps,
        "output_dir":output_dir,
        "save_name":save_name,
        "train_data_dir":train_data_dir,
        "optimizer":optimizer,
        "lr_scheduler":lr_scheduler,
        "learning_rate":learning_rate,
        "train_batch_size":train_batch_size,
        "repeats":repeats,
        "gradient_accumulation_steps":gradient_accumulation_steps,
        "num_train_epochs":num_train_epochs,
        "save_model_epochs":save_model_epochs,
        "validation_epochs":validation_epochs,
        "rank":rank,
        "skip_epoch":skip_epoch,
        # "break_epoch":break_epoch,
        "skip_step":skip_step,
        "gradient_checkpointing":gradient_checkpointing,
        "validation_ratio":validation_ratio,
        "pretrained_model_name_or_path":pretrained_model_name_or_path,
        "model_path":model_path,
        "resume_from_checkpoint":resume_from_checkpoint,
        # "use_dora":use_dora,
        "recreate_cache":recreate_cache,
        # "vae_path":vae_path,
        "config_path":filename,  # Store relative filename
        "resolution":resolution,
        # "use_debias":use_debias,
        # 'snr_gamma':snr_gamma,
        "caption_dropout":caption_dropout,
        "cosine_restarts":cosine_restarts,
        "max_time_steps":max_time_steps,
        # "freeze_transformer_layers":freeze_transformer_layers
        "blocks_to_swap":blocks_to_swap,
        "mask_dropout":mask_dropout,
        "reg_ratio":reg_ratio,
        "reg_timestep":reg_timestep
        # "use_fp8":use_fp8
    }
    
    # Save to configs directory
    with open(full_config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {full_config_path}")
    
    # Also save a copy as default config.json for backward compatibility
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=4)

# 获取配置文件列表
def get_config_files():
    """获取configs目录中所有JSON文件的列表（包括子目录）"""
    configs_dir = os.path.join(os.getcwd(), "configs")
    if not os.path.exists(configs_dir):
        return ["config.json"]
    
    json_files = []
    
    # 递归搜索所有子目录
    for root, dirs, files in os.walk(configs_dir):
        for file in files:
            if file.endswith('.json'):
                # 计算相对路径
                rel_path = os.path.relpath(os.path.join(root, file), configs_dir)
                json_files.append(rel_path)
    
    return sorted(json_files) if json_files else ["config.json"]

# Function to load configuration from a file path
def load_config_from_file(config_path_input):
    """
    从文件加载配置
    config_path_input: 配置文件路径输入框的值
    """
    if config_path_input is None or config_path_input.strip() == "":
        print("No config path provided")
        return None
    
    config_path = config_path_input.strip()
    
    # 如果路径不是绝对路径，尝试从当前目录或configs目录加载
    if not os.path.isabs(config_path):
        # 先尝试当前目录
        if os.path.exists(config_path):
            config_path = config_path
        else:
            # 再尝试configs目录
            configs_dir = os.path.join(os.getcwd(), "configs")
            configs_path = os.path.join(configs_dir, config_path)
            if os.path.exists(configs_path):
                config_path = configs_path
            else:
                print(f"Config file not found: {config_path}")
                return None
    
    # 加载配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"Loaded configuration from {config_path}")
    except Exception as e:
        print(f"Error loading config: {e}")
        return None
    
    # 返回加载的配置值
    return [
        config_path_input,
        config.get('script', page_config['script']),
        config.get('seed', page_config['seed']),
        config.get('mixed_precision', page_config['mixed_precision']),
        config.get('report_to', page_config['report_to']),
        config.get('lr_warmup_steps', page_config['lr_warmup_steps']),
        config.get('output_dir', page_config['output_dir']),
        config.get('save_name', page_config['save_name']),
        config.get('train_data_dir', page_config['train_data_dir']),
        config.get('optimizer', page_config['optimizer']),
        config.get('lr_scheduler', page_config['lr_scheduler']),
        config.get('learning_rate', page_config['learning_rate']),
        config.get('train_batch_size', page_config['train_batch_size']),
        config.get('repeats', page_config['repeats']),
        config.get('gradient_accumulation_steps', page_config['gradient_accumulation_steps']),
        config.get('num_train_epochs', page_config['num_train_epochs']),
        config.get('save_model_epochs', page_config['save_model_epochs']),
        config.get('validation_epochs', page_config['validation_epochs']),
        config.get('rank', page_config['rank']),
        config.get('skip_epoch', page_config['skip_epoch']),
        config.get('skip_step', page_config['skip_step']),
        config.get('gradient_checkpointing', page_config['gradient_checkpointing']),
        config.get('validation_ratio', page_config['validation_ratio']),
        config.get('pretrained_model_name_or_path', page_config['pretrained_model_name_or_path']),
        config.get('model_path', page_config['model_path']),
        config.get('resume_from_checkpoint', page_config['resume_from_checkpoint']),
        config.get('recreate_cache', page_config['recreate_cache']),
        config.get('resolution', page_config['resolution']),
        config.get('caption_dropout', page_config['caption_dropout']),
        config.get('cosine_restarts', page_config['cosine_restarts']),
        config.get('max_time_steps', page_config['max_time_steps']),
        config.get('blocks_to_swap', page_config['blocks_to_swap']),
        config.get('mask_dropout', page_config['mask_dropout']),
        config.get('reg_ratio', page_config['reg_ratio']),
        config.get('reg_timestep', page_config['reg_timestep'])
    ]
        # default_config['use_dora'], \
        # default_config['freeze_transformer_layers']
        # default_config['logging_dir'],default_config['break_epoch'], 

# 下载配置文件功能
def download_config_file(config_path_input):
    """
    下载配置文件
    config_path_input: 配置文件路径输入框的值
    """
    if config_path_input is None or config_path_input.strip() == "":
        print("No config path provided")
        return None
    
    config_path = config_path_input.strip()
    
    # 如果路径不是绝对路径，尝试从当前目录或configs目录加载
    if not os.path.isabs(config_path):
        # 先尝试当前目录
        if os.path.exists(config_path):
            config_path = config_path
        else:
            # 再尝试configs目录
            configs_dir = os.path.join(os.getcwd(), "configs")
            configs_path = os.path.join(configs_dir, config_path)
            if os.path.exists(configs_path):
                config_path = configs_path
            else:
                print(f"Config file not found: {config_path}")
                return None
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return None
    
    # 返回文件路径供下载
    print(f"Preparing to download: {config_path}")
    return config_path

# 下载配置文件功能（用于按钮点击）
def download_config_file_for_button(config_path_input):
    """
    下载配置文件
    config_path_input: 配置文件路径输入框的值
    """
    if config_path_input is None or config_path_input.strip() == "":
        return gr.update(value=None, visible=False)
    
    config_path = config_path_input.strip()
    
    # 如果路径不是绝对路径，尝试从当前目录或configs目录加载
    if not os.path.isabs(config_path):
        # 先尝试当前目录
        if os.path.exists(config_path):
            config_path = config_path
        else:
            # 再尝试configs目录
            configs_dir = os.path.join(os.getcwd(), "configs")
            configs_path = os.path.join(configs_dir, config_path)
            if os.path.exists(configs_path):
                config_path = configs_path
            else:
                return gr.update(value=None, visible=False)
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        return gr.update(value=None, visible=False)
    
    # 返回文件路径并显示下载链接
    print(f"Preparing to download: {config_path}")
    return gr.update(value=config_path, visible=True)

# 注释掉自动加载配置功能
# load_config_from_file(None)

def run(
        config_path,
        script,
        seed,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        recreate_cache,
        resolution,
        caption_dropout,
        cosine_restarts,
        max_time_steps,
        blocks_to_swap,
        mask_dropout,
        reg_ratio,
        reg_timestep
    ):
    # Save the current configuration to the specified config file
    save_config(
        config_path,
        script,
        seed,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        recreate_cache,
        resolution,
        caption_dropout,
        cosine_restarts,
        max_time_steps,
        blocks_to_swap,
        mask_dropout,
        reg_ratio,
        reg_timestep
    )

    # Construct the command to run the script with only the config path
    command_args = [sys.executable, script, "--config_path", config_path]

    # Execute the command
    subprocess.call(command_args)

    # Return the executed command as a string
    return " ".join(command_args)

def toggle_language_handler():
    """语言切换处理函数"""
    toggle_language()
    # 返回更新后的组件
    updates = []
    # 更新标题
    updates.append(gr.Markdown(get_text('title')))
    # 更新语言切换按钮文本
    updates.append(gr.Button(get_text('language_toggle'), scale=0, size="sm"))
    return updates

def update_language_interface():
    """更新界面语言，返回所有需要更新的组件"""
    toggle_language()
    # 返回更新后的所有UI组件
    updated_components = [
        # 基础组件
        gr.Markdown(get_text('title')),  # 标题
        gr.Button(get_text('refresh'), scale=0, size="sm", min_width=50),  # 刷新按钮
        gr.Button(get_text('language_toggle'), scale=0, size="sm"),  # 语言切换按钮
        gr.Dropdown(label=get_text('script'), value=page_config["script"], choices=page_config["script_choices"]),  # 脚本选择
        gr.Textbox(label=get_text('config_path'), value=page_config["config_path"]),  # 配置路径
        gr.Button(get_text('load'), scale=1, variant="primary"),  # 加载按钮
        gr.Button(get_text('save'), scale=1, variant="secondary"),  # 下载按钮
        gr.File(label=get_text('download_link'), visible=False),  # 下载链接组件
        # 目录设置部分的组件
        gr.Textbox(label=get_text('output_dir'), value=page_config["output_dir"], placeholder=get_text('output_dir_placeholder')),  # 输出目录
        gr.Textbox(label=get_text('save_name'), value=page_config["save_name"], placeholder=get_text('save_name_placeholder')),  # 保存名称
        gr.Textbox(label=get_text('pretrained_model_name_or_path'), value=page_config["pretrained_model_name_or_path"], placeholder=get_text('pretrained_model_name_or_path_placeholder')),  # 预训练模型路径
        gr.Textbox(label=get_text('resume_from_checkpoint'), value=page_config["resume_from_checkpoint"], placeholder=get_text('resume_from_checkpoint_placeholder')),  # 恢复检查点
        gr.Textbox(label=get_text('train_data_dir'), value=page_config["train_data_dir"], placeholder=get_text('train_data_dir_placeholder')),  # 训练数据目录
        gr.Textbox(label=get_text('model_path'), value=page_config["model_path"], placeholder=get_text('model_path_placeholder')),  # 模型路径
        gr.Dropdown(label=get_text('report_to'), value=page_config["report_to"], choices=["all","wandb","tensorboard"]),  # 报告到
        # LoRA配置部分的组件
        gr.Number(label=get_text('rank'), value=page_config["rank"], info=get_text('rank_info')),  # 排名
        gr.Number(label=get_text('train_batch_size'), value=page_config["train_batch_size"], info=get_text('train_batch_size_info')),  # 训练批次大小
        gr.Number(label=get_text('repeats'), value=page_config["repeats"]),  # 重复次数
        gr.Number(label=get_text('gradient_accumulation_steps'), value=page_config["gradient_accumulation_steps"]),  # 梯度累积步数
        gr.Radio(label=get_text('mixed_precision'), value=page_config["mixed_precision"], choices=["bf16", "fp8"]),  # 混合精度
        gr.Checkbox(label=get_text('gradient_checkpointing'), value=page_config["gradient_checkpointing"]),  # 梯度检查点
        gr.Dropdown(label=get_text('optimizer'), value=page_config["optimizer"], choices=["adamw","prodigy"]),  # 优化器
        gr.Dropdown(label=get_text('lr_scheduler'), value=page_config["lr_scheduler"], choices=["linear", "cosine", "cosine_with_restarts", "polynomial","constant", "constant_with_warmup"]),  # 学习率调度器
        gr.Number(label=get_text('cosine_restarts'), value=page_config["cosine_restarts"], info=get_text('cosine_restarts_info'), minimum=1),  # 余弦重启
        gr.Number(label=get_text('learning_rate'), value=page_config["learning_rate"], info=get_text('learning_rate_info')),  # 学习率
        gr.Number(label=get_text('lr_warmup_steps'), value=page_config["lr_warmup_steps"]),  # 学习率预热步数
        gr.Number(label=get_text('seed'), value=page_config["seed"]),  # 随机种子
        gr.Number(label=get_text('blocks_to_swap'), value=page_config["blocks_to_swap"], info=get_text('blocks_to_swap_info')),  # 交换块数
        gr.Number(label=get_text('mask_dropout'), value=page_config["mask_dropout"], info=get_text('mask_dropout_info')),  # 掩码丢弃
        gr.Number(label=get_text('reg_ratio'), value=page_config["reg_ratio"], info=get_text('reg_ratio_info')),  # 正则化比率
        gr.Number(label=get_text('reg_timestep'), value=page_config["reg_timestep"], info=get_text('reg_timestep_info')),  # 正则化时间步
        # Misc部分的组件
        gr.Number(label=get_text('num_train_epochs'), value=page_config["num_train_epochs"], info=get_text('num_train_epochs_info')),  # 训练轮数
        gr.Number(label=get_text('save_model_epochs'), value=page_config["save_model_epochs"], info=get_text('save_model_epochs_info')),  # 保存模型轮数
        gr.Number(label=get_text('validation_epochs'), value=page_config["validation_epochs"], info=get_text('validation_epochs_info')),  # 验证轮数
        gr.Number(label=get_text('skip_epoch'), value=page_config["skip_epoch"], info=get_text('skip_epoch_info')),  # 跳过轮数
        gr.Number(label=get_text('skip_step'), value=page_config["skip_step"], info=get_text('skip_step_info')),  # 跳过步数
        gr.Number(label=get_text('validation_ratio'), value=page_config["validation_ratio"], info=get_text('validation_ratio_info')),  # 验证比率
        gr.Checkbox(label=get_text('recreate_cache'), value=page_config["recreate_cache"]),  # 重建缓存
        gr.Number(label=get_text('caption_dropout'), value=page_config["caption_dropout"], info=get_text('caption_dropout_info'), maximum=1, minimum=0),  # 标题丢弃
        gr.Number(label=get_text('max_time_steps'), value=page_config["max_time_steps"], info=get_text('max_time_steps_info'), maximum=1000, minimum=0),  # 最大时间步
        gr.Markdown(get_text('resolution_section')),  # 分辨率说明
        gr.Dropdown(label=get_text('resolution'), value=page_config["resolution"], choices=page_config["resolution_choices"]),  # 分辨率
        # 输出和运行按钮
        gr.Textbox(label=get_text('output_box')),  # 输出框
        gr.Button(get_text('run_button'))  # 运行按钮
    ]
    return updated_components
    
# 处理文件上传事件
def handle_file(file_obj):
    if file_obj is None:
        return ""
    
    # 创建configs目录
    configs_dir = os.path.join(os.getcwd(), "configs")
    os.makedirs(configs_dir, exist_ok=True)
    
    # 按日期创建子目录 (格式: YYYY-MM-DD)
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_dir = os.path.join(configs_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)
    
    # 获取原始文件名
    original_filename = os.path.basename(file_obj.name)
    if not original_filename.endswith(".json"):
        original_filename += ".json"
    
    # 添加时间戳避免文件名冲突
    timestamp = datetime.now().strftime("%H%M%S")
    name_without_ext = os.path.splitext(original_filename)[0]
    new_filename = f"{name_without_ext}_{timestamp}.json"
    
    # 构建目标路径
    target_path = os.path.join(date_dir, new_filename)
    
    try:
        # 复制文件到目标目录
        import shutil
        shutil.copy2(file_obj.name, target_path)
        print(f"文件已保存到: {target_path}")
        
        # 返回相对路径 (相对于configs目录)
        relative_path = os.path.join(date_str, new_filename)
        return relative_path
        
    except Exception as e:
        print(f"保存文件时出错: {e}")
        # 如果保存失败，返回原始文件路径
        return file_obj.name

# 创建UI界面
with gr.Blocks(css=css_code) as demo:
    # 语言切换按钮和刷新按钮
    with gr.Row():
        gr.HTML("<div style='flex-grow: 1;'></div>")  # 占位符，让按钮右对齐
        refresh_config_btn = gr.Button(get_text('refresh'), scale=0, size="sm", min_width=50)
        language_toggle_btn = gr.Button(get_text('language_toggle'), scale=0, size="sm", min_width=100)
    
    # 标题
    title_md = gr.Markdown(get_text('title'))

     # 上传配置文件
    config_file_upload = gr.File(label=get_text('upload_config_file'), file_types=[".json"], file_count="single", scale=1, elem_classes="my-file-upload")
    config_path = gr.Textbox(label=get_text('config_file_path'), value=page_config["config_path"], placeholder="输入配置文件路径或上传文件")

    # 配置文件操作按钮
    with gr.Row(equal_height=True):
        load_config_btn = gr.Button(get_text('load'), scale=1, variant="primary")
        download_btn = gr.Button(get_text('save'), scale=1, variant="secondary")
    
    download_file = gr.File(label=get_text('download_link'), visible=False)

    gr.HTML("<div style='border-bottom: 2px dotted #e0e0e0; flex-grow: 1;'></div>")

    # 脚本选择
    script = gr.Dropdown(label=get_text('script'), value=page_config["script"], choices=page_config["script_choices"])
    
    directory_accordion = gr.Accordion(get_text('directory_section'))
    with directory_accordion:
        # 目录设置部分
        with gr.Row():
            output_dir = gr.Textbox(label=get_text('output_dir'), value=page_config["output_dir"],
                                   placeholder=get_text('output_dir_placeholder'))
            save_name = gr.Textbox(label=get_text('save_name'), value=page_config["save_name"],
                                   placeholder=get_text('save_name_placeholder'))
        with gr.Row():
            pretrained_model_name_or_path = gr.Textbox(label=get_text('pretrained_model_name_or_path'), 
                value=page_config["pretrained_model_name_or_path"], 
                placeholder=get_text('pretrained_model_name_or_path_placeholder')
            )
            resume_from_checkpoint = gr.Textbox(label=get_text('resume_from_checkpoint'), value=page_config["resume_from_checkpoint"], placeholder=get_text('resume_from_checkpoint_placeholder'))
        with gr.Row():
            train_data_dir = gr.Textbox(label=get_text('train_data_dir'), value=page_config["train_data_dir"], placeholder=get_text('train_data_dir_placeholder'))
            model_path = gr.Textbox(label=get_text('model_path'), value=page_config["model_path"], placeholder=get_text('model_path_placeholder'))
        with gr.Row():
            report_to = gr.Dropdown(label=get_text('report_to'), value=page_config["report_to"], choices=["all","wandb","tensorboard"])

    lora_accordion = gr.Accordion(get_text('lora_config'))
    with lora_accordion:
        # 训练相关设置
        with gr.Row():
            rank = gr.Number(label=get_text('rank'), value=page_config["rank"], info=get_text('rank_info'))
            train_batch_size = gr.Number(label=get_text('train_batch_size'), value=page_config["train_batch_size"], info=get_text('train_batch_size_info'))
        with gr.Row():
            repeats = gr.Number(label=get_text('repeats'), value=page_config["repeats"])
            gradient_accumulation_steps = gr.Number(label=get_text('gradient_accumulation_steps'), value=page_config["gradient_accumulation_steps"])
            mixed_precision = gr.Radio(label=get_text('mixed_precision'), value=page_config["mixed_precision"], choices=["bf16", "fp8"])
            gradient_checkpointing = gr.Checkbox(label=get_text('gradient_checkpointing'), value=page_config["gradient_checkpointing"])
        with gr.Row():
            optimizer = gr.Dropdown(label=get_text('optimizer'), value=page_config["optimizer"], choices=["adamw","prodigy"])
            lr_scheduler = gr.Dropdown(label=get_text('lr_scheduler'), value=page_config["lr_scheduler"], 
                        choices=["linear", "cosine", "cosine_with_restarts", "polynomial","constant", "constant_with_warmup"])
            cosine_restarts = gr.Number(label=get_text('cosine_restarts'), value=page_config["cosine_restarts"], info=get_text('cosine_restarts_info'), minimum=1)
        with gr.Row():
            learning_rate = gr.Number(label=get_text('learning_rate'), value=page_config["learning_rate"], info=get_text('learning_rate_info'))
            lr_warmup_steps = gr.Number(label=get_text('lr_warmup_steps'), value=page_config["lr_warmup_steps"])
            seed = gr.Number(label=get_text('seed'), value=page_config["seed"])
        with gr.Row():
            blocks_to_swap = gr.Number(label=get_text('blocks_to_swap'), value=page_config["blocks_to_swap"], info=get_text('blocks_to_swap_info'))
            mask_dropout = gr.Number(label=get_text('mask_dropout'), value=page_config["mask_dropout"], info=get_text('mask_dropout_info'))
            reg_ratio = gr.Number(label=get_text('reg_ratio'), value=page_config["reg_ratio"], info=get_text('reg_ratio_info'))
            reg_timestep = gr.Number(label=get_text('reg_timestep'), value=page_config["reg_timestep"], info=get_text('reg_timestep_info'))
            
    misc_accordion = gr.Accordion(get_text('misc'))
    with misc_accordion:
        with gr.Row():
            num_train_epochs = gr.Number(label=get_text('num_train_epochs'), value=page_config["num_train_epochs"], info=get_text('num_train_epochs_info'))
            save_model_epochs = gr.Number(label=get_text('save_model_epochs'), value=page_config["save_model_epochs"], info=get_text('save_model_epochs_info'))
            validation_epochs = gr.Number(label=get_text('validation_epochs'), value=page_config["validation_epochs"], info=get_text('validation_epochs_info'))
        with gr.Row():
            skip_epoch = gr.Number(label=get_text('skip_epoch'), value=page_config["skip_epoch"], info=get_text('skip_epoch_info'))
            skip_step = gr.Number(label=get_text('skip_step'), value=page_config["skip_step"], info=get_text('skip_step_info'))
            validation_ratio = gr.Number(label=get_text('validation_ratio'), value=page_config["validation_ratio"], info=get_text('validation_ratio_info'))
            
        with gr.Row():
            recreate_cache = gr.Checkbox(label=get_text('recreate_cache'), value=page_config["recreate_cache"])
            caption_dropout = gr.Number(label=get_text('caption_dropout'), value=page_config["caption_dropout"], info=get_text('caption_dropout_info'), maximum=1, minimum=0)
            max_time_steps = gr.Number(label=get_text('max_time_steps'), value=page_config["max_time_steps"], info=get_text('max_time_steps_info'), maximum=1000, minimum=0)
        
        resolution_md = gr.Markdown(get_text('resolution_section'))
        with gr.Row():
            resolution = gr.Dropdown(label=get_text('resolution'), value=page_config["resolution"], choices=page_config["resolution_choices"])
    
    # 输出和运行按钮
    output = gr.Textbox(label=get_text('output_box'))
    run_btn = gr.Button(get_text('run_button'), variant="primary")
    
    # 定义所有输入组件列表
    inputs = [
        config_path,
        script,
        seed,
        # logging_dir,
        mixed_precision,
        report_to,
        lr_warmup_steps,
        output_dir,
        save_name,
        train_data_dir,
        optimizer,
        lr_scheduler,
        learning_rate,
        train_batch_size,
        repeats,
        gradient_accumulation_steps,
        num_train_epochs,
        save_model_epochs,
        validation_epochs,
        rank,
        skip_epoch,
        # break_epoch,
        skip_step,
        gradient_checkpointing,
        validation_ratio,
        pretrained_model_name_or_path,
        model_path,
        resume_from_checkpoint,
        # use_dora,
        recreate_cache,
        # vae_path,
        resolution,
        # use_debias,
        # snr_gamma,
        caption_dropout,
        cosine_restarts,
        max_time_steps,
        blocks_to_swap,
        mask_dropout,
        reg_ratio,
        reg_timestep
        # freeze_transformer_layers,
    ]
    
    # 绑定事件处理器
    run_btn.click(fn=run, inputs=inputs, outputs=output, api_name="run")

    # 绑定加载配置事件 - 只从路径读取
    load_config_btn.click(fn=load_config_from_file, inputs=[config_path], outputs=[
        config_path, script, seed, mixed_precision, report_to, lr_warmup_steps,
        output_dir, save_name, train_data_dir, optimizer, lr_scheduler, learning_rate,
        train_batch_size, repeats, gradient_accumulation_steps, num_train_epochs, 
        save_model_epochs, validation_epochs, rank, skip_epoch, skip_step, 
        gradient_checkpointing, validation_ratio, pretrained_model_name_or_path, 
        model_path, resume_from_checkpoint, recreate_cache, resolution,
        caption_dropout, cosine_restarts, max_time_steps, blocks_to_swap, 
        mask_dropout, reg_ratio, reg_timestep
    ])

    # 绑定下载配置事件
    download_btn.click(
        fn=download_config_file_for_button,
        inputs=[config_path],
        outputs=[download_file]
    )

    # 绑定文件上传事件 - 上传后自动更新路径
    config_file_upload.change(fn=handle_file, inputs=config_file_upload, outputs=config_path)

    # 语言切换事件处理 - 更新所有组件
    language_toggle_btn.click(
        fn=update_language_interface,
        inputs=[],
        outputs=[
            title_md, refresh_config_btn, language_toggle_btn, script, config_path, load_config_btn, download_btn, download_file,
            output_dir, save_name, pretrained_model_name_or_path, resume_from_checkpoint, 
            train_data_dir, model_path, report_to,
            rank, train_batch_size, repeats, gradient_accumulation_steps, mixed_precision, gradient_checkpointing,
            optimizer, lr_scheduler, cosine_restarts, learning_rate, lr_warmup_steps, seed,
            blocks_to_swap, mask_dropout, reg_ratio, reg_timestep,
            num_train_epochs, save_model_epochs, validation_epochs, skip_epoch, skip_step, validation_ratio,
            recreate_cache, caption_dropout, max_time_steps, resolution_md, resolution,
            output, run_btn
        ]
    )

# 启动界面
if __name__ == "__main__":
    demo.launch(
        server_port=6006,
    )