# -*- coding: utf-8 -*-
"""
多语言翻译文件
包含所有界面文本的中英文翻译
"""

# 翻译字典 - 包含所有需要翻译的文本
TRANSLATIONS = {
    'zh': {
        'title': '## LoRA 训练',
        'script': '训练脚本',
        'config_path': '配置文件路径 (.json文件)',
        'config_path_placeholder': '输入保存/加载配置的路径',
        'config_file_path': '配置文件路径',
        'save': '下载配置',
        'load': '加载配置',
        'directory_section': '目录配置',
        'output_dir': '输出目录',
        'output_dir_placeholder': '检查点保存位置',
        'save_name': '保存名称',
        'save_name_placeholder': '检查点保存名称',
        'pretrained_model_name_or_path': '预训练模型名称或路径',
        'pretrained_model_name_or_path_placeholder': '仓库名称或包含diffusers模型结构的目录',
        'resume_from_checkpoint': '从检查点恢复',
        'resume_from_checkpoint_placeholder': '从选定目录恢复lora权重',
        'train_data_dir': '训练数据目录',
        'train_data_dir_placeholder': '包含数据集的目录',
        'model_path': '模型路径',
        'model_path_placeholder': '如果不是从官方权重训练则为单个权重文件',
        'report_to': '报告到',
        'lora_config': 'LoRA 配置',
        'rank': '秩',
        'rank_info': '建议对小于100的训练集使用秩4',
        'train_batch_size': '训练批次大小',
        'train_batch_size_info': '批次大小1使用18GB。请使用小批次大小以避免内存不足',
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
        'download_link': '下载链接',
    },
    'en': {
        'title': '## Lora Training',
        'script': 'script',
        'config_path': 'Config Path (.json file)',
        'config_path_placeholder': 'Enter path to save/load config',
        'config_file_path': 'Config File Path',
        'save': 'Download Config',
        'load': 'Load Config',
        'directory_section': 'Directory section',
        'output_dir': 'output_dir',
        'output_dir_placeholder': 'checkpoint save to',
        'save_name': 'save_name',
        'save_name_placeholder': 'checkpoint save name',
        'pretrained_model_name_or_path': 'pretrained_model_name_or_path',
        'pretrained_model_name_or_path_placeholder': 'repo name or dir contains diffusers model structure',
        'resume_from_checkpoint': 'resume_from_checkpoint',
        'resume_from_checkpoint_placeholder': 'resume the lora weight from seleted dir',
        'train_data_dir': 'train_data_dir',
        'train_data_dir_placeholder': 'dir contains dataset',
        'model_path': 'model_path',
        'model_path_placeholder': 'single weight files if not trained from official weight',
        'report_to': 'report_to',
        'lora_config': 'Lora Config',
        'rank': 'rank',
        'rank_info': 'Recommanded to use rank 4 for training set small than 100.',
        'train_batch_size': 'train_batch_size',
        'train_batch_size_info': 'Batch size 1 is using 18GB. Please use small batch size to avoid oom.',
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
        'download_link': 'Download Link',
    }
}

# 支持的语言列表
SUPPORTED_LANGUAGES = ['zh', 'en']

# 默认语言
DEFAULT_LANGUAGE = 'en'

def get_text(key, language=None):
    """
    获取指定语言的文本
    
    Args:
        key (str): 文本键名
        language (str, optional): 语言代码，如果为None则使用默认语言
    
    Returns:
        str: 对应的翻译文本，如果找不到则返回键名本身
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    if language not in TRANSLATIONS:
        language = DEFAULT_LANGUAGE
    
    return TRANSLATIONS[language].get(key, key)

def get_supported_languages():
    """
    获取支持的语言列表
    
    Returns:
        list: 支持的语言代码列表
    """
    return SUPPORTED_LANGUAGES.copy()

def is_supported_language(language):
    """
    检查是否为支持的语言
    
    Args:
        language (str): 语言代码
    
    Returns:
        bool: 是否为支持的语言
    """
    return language in SUPPORTED_LANGUAGES 