import gradio as gr

import subprocess
import json
import sys
import os
from dataset_upload import add_dataset_upload_tab

# ===== 语言翻译系统 =====
# 翻译字典 - 包含所有需要翻译的文本
TRANSLATIONS = {
    'zh': {
        'title': '## LoRA 训练',
        'script': '训练脚本',
        'config_path': '配置文件路径 (.json文件)',
        'config_path_placeholder': '输入保存/加载配置的路径',
        'save': '保存',
        'load': '加载',
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
        'language_toggle': '🌐 切换到English',
        
        'slider': '滑块训练相关',
        'use_two_captions': '使用两对应文本标注',
        'slider_positive_scale': '滑块正向目标强度',
        'slider_negative_scale': '滑块负面目标强度',
        
        'dataset_upload': '数据集上传',
        'upload_training_dataset': '## 上传训练数据集',
        'upload_dataset_description': '上传您的数据集压缩包（zip、tar、tar.gz等），系统将自动解压和验证。',
        'dataset_archive': '数据集压缩包',
        'dataset_name': '数据集名称',
        'dataset_name_placeholder': '为此数据集输入名称（例如：my_dataset）',
        'upload_dataset_btn': '上传数据集',
        'upload_status': '上传状态',
        'dataset_path': '数据集路径',
        
        'dataset_requirements': '### 数据集要求：',
        'dataset_requirements_content': '压缩包必须包含图像文件（jpg、jpeg、png、bmp、webp）和对应的文本文件（txt、caption）\\n每张图像应有相同名称的文本文件包含描述\\n示例结构：\\n```\\ndataset/\\n├── image1.jpg\\n├── image1.txt\\n├── image2.png\\n├── image2.txt\\n└── ...\\n```'
    },
    'en': {
        'title': '## Lora Training',
        'script': 'script',
        'config_path': 'Config Path (.json file)',
        'config_path_placeholder': 'Enter path to save/load config',
        'save': 'Save',
        'load': 'load',
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
        'language_toggle': '🌐 切换到中文',
        
        
        'slider': 'Slider Related',
        'use_two_captions': 'Use two captions for each direction',
        'slider_positive_scale': 'Slider positive scale',
        'slider_negative_scale': 'Slider negative scale',
        
        'dataset_upload': 'Dataset Upload',
        'upload_training_dataset': '## Upload Training Dataset',
        'upload_dataset_description': 'Upload your dataset archive (zip, tar, tar.gz, etc.) and it will be automatically extracted and validated.',
        'dataset_archive': 'Dataset Archive',
        'dataset_name': 'Dataset Name',
        'dataset_name_placeholder': 'Enter a name for this dataset (e.g., my_dataset)',
        'upload_dataset_btn': 'Upload Dataset',
        'upload_status': 'Upload Status',
        'dataset_path': 'Dataset Path',
        
        'dataset_requirements': '### Dataset Requirements:',
        'dataset_requirements_content': 'Archive must contain image files (jpg, jpeg, png, bmp, webp) and corresponding text files (txt, caption)\\nEach image should have a text file with the same name containing the caption\\nExample structure:\\n```\\ndataset/\\n├── image1.jpg\\n├── image1.txt\\n├── image2.png\\n├── image2.txt\\n└── ...\\n```'
    }
}

# 当前语言状态
current_language = 'en'  # 默认中文

def get_text(key):
    """获取当前语言的文本"""
    return TRANSLATIONS[current_language].get(key, key)

def toggle_language():
    """切换语言"""
    global current_language
    current_language = 'en' if current_language == 'zh' else 'zh'
    return current_language

default_config = {
    "script": "train_flux_lora_ui_kontext.py",
    "script_choices": [
                        "train_flux_lora_ui_kontext.py",
                        "train_flux_lora_ui_kontext_slider.py",
                        "train_flux_lora_ui_with_mask.py",
                        "train_flux_lora_ui.py",
                       ],
    "output_dir":"F:/models/flux",
    "save_name":"flux-lora",
    "pretrained_model_name_or_path":"F:/T2ITrainer/flux_models/kontext", # or local folder F:\Kolors
    "train_data_dir":"F:/ImageSet/kontext", 
    # "vae_path":None, # or local file
    "resume_from_checkpoint":None,
    "model_path":None, 
    # "logging_dir":"logs",
    "report_to":"all", 
    "rank":16,
    "train_batch_size":1,
    "repeats":1,
    "gradient_accumulation_steps":1,
    "mixed_precision":"bf16",
    "gradient_checkpointing":True,
    "optimizer":"adamw",
    "lr_scheduler":"constant", 
    "learning_rate":1e-4,
    "lr_warmup_steps":0,
    "seed":4321,
    "num_train_epochs":5,
    "save_model_epochs":1, 
    "validation_epochs":1, 
    "skip_epoch":0, 
    # "break_epoch":0,
    "skip_step":0, 
    "validation_ratio":0.1, 
    # "use_dora":False,
    "recreate_cache":False,
    "caption_dropout":0.1,
    "config_path":"config.json",
    "resolution":"512",
    "resolution_choices":["512","256","1024"],
    "use_debias":False,
    "snr_gamma":0,
    "cosine_restarts":1,
    "max_time_steps":0,
    "blocks_to_swap":0,
    "mask_dropout":0,
    "reg_ratio":0.0,
    "reg_timestep":0,
    'use_two_captions': False,
    'slider_positive_scale': 1.0,
    'slider_negative_scale': -1.0
    # "use_fp8":True
    # "freeze_transformer_layers":'5,7,10,17,18,19'
}


# Function to save configuration to a specified directory
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
        reg_timestep,
        use_two_captions,
        slider_positive_scale,
        slider_negative_scale
        # use_fp8
        # freeze_transformer_layers
    ):
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
        "config_path":config_path,
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
        "reg_timestep":reg_timestep,
        'use_two_captions': use_two_captions,
        'slider_positive_scale': slider_positive_scale,
        'slider_negative_scale': slider_negative_scale
        # "use_fp8":use_fp8
    }
    # config_path = os.path.join(config_dir, f"{filename}{ext}")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {config_path}")
    print(f"Update default config")
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=4)

# Function to load configuration from a specified directory
def load_config(config_path):
    if not config_path.endswith(".json"):
        print("!!!File is not json format.")
        print("Load default config")
        config_path = "config.json"
    if not os.path.exists(config_path):
        # create config
        with open(config_path, 'w') as f:
            config = {}
            for key in default_config.keys():
                config[key] = default_config[key]
            json.dump(config, f, indent=4)
        return config
    config_path = os.path.join(config_path)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        config_path = "config.json"
    print(f"Loaded configuration from {config_path}")
    # print("config")
    # print(config)
    for key in config.keys():
        default_config[key] = config[key]
            
    # print("default_config")
    # print(default_config)
    return config_path,default_config['script'],default_config['seed'], \
            default_config['mixed_precision'],default_config['report_to'],default_config['lr_warmup_steps'], \
            default_config['output_dir'],default_config['save_name'],default_config['train_data_dir'], \
            default_config['optimizer'],default_config['lr_scheduler'],default_config['learning_rate'], \
            default_config['train_batch_size'],default_config['repeats'],default_config['gradient_accumulation_steps'], \
            default_config['num_train_epochs'],default_config['save_model_epochs'],default_config['validation_epochs'], \
            default_config['rank'],default_config['skip_epoch'], \
            default_config['skip_step'],default_config['gradient_checkpointing'],default_config['validation_ratio'], \
            default_config['pretrained_model_name_or_path'],default_config['model_path'],default_config['resume_from_checkpoint'], \
            default_config['recreate_cache'],default_config['resolution'], \
            default_config['caption_dropout'], \
            default_config['cosine_restarts'],default_config['max_time_steps'], \
            default_config['blocks_to_swap'],default_config['mask_dropout'], \
            default_config['reg_ratio'],default_config['reg_timestep'], \
            default_config['use_two_captions'],default_config['slider_positive_scale'],default_config['slider_negative_scale']
            # default_config['use_dora'], \
            # default_config['freeze_transformer_layers']
            # default_config['logging_dir'],default_config['break_epoch'], 

# load config.json by default
load_config("config.json")
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
        reg_timestep,
        use_two_captions,
        slider_positive_scale,
        slider_negative_scale
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
        reg_timestep,
        use_two_captions,
        slider_positive_scale,
        slider_negative_scale
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

# 创建UI界面
with gr.Blocks() as demo:
    # 语言切换按钮
    with gr.Row():
        gr.HTML("<div style='flex-grow: 1;'></div>")  # 占位符，让按钮右对齐
        language_toggle_btn = gr.Button(get_text('language_toggle'), scale=0, size="sm")
    
    # 标题
    title_md = gr.Markdown(get_text('title'))
    
    # 脚本选择
    script = gr.Dropdown(label=get_text('script'), value=default_config["script"], choices=default_config["script_choices"])
    
    # 配置文件操作
    with gr.Row(equal_height=True):
        config_path = gr.Textbox(scale=3, label=get_text('config_path'), value=default_config["config_path"], placeholder=get_text('config_path_placeholder'))
        save_config_btn = gr.Button(get_text('save'), scale=1)
        load_config_btn = gr.Button(get_text('load'), scale=1)

    directory_accordion = gr.Accordion(get_text('directory_section'))
    with directory_accordion:
        # 目录设置部分
        with gr.Row():
            output_dir = gr.Textbox(label=get_text('output_dir'), value=default_config["output_dir"],
                                   placeholder=get_text('output_dir_placeholder'))
            save_name = gr.Textbox(label=get_text('save_name'), value=default_config["save_name"],
                                   placeholder=get_text('save_name_placeholder'))
        with gr.Row():
            pretrained_model_name_or_path = gr.Textbox(label=get_text('pretrained_model_name_or_path'), 
                value=default_config["pretrained_model_name_or_path"], 
                placeholder=get_text('pretrained_model_name_or_path_placeholder')
            )
            resume_from_checkpoint = gr.Textbox(label=get_text('resume_from_checkpoint'), value=default_config["resume_from_checkpoint"], placeholder=get_text('resume_from_checkpoint_placeholder'))
        with gr.Row():
            train_data_dir = gr.Textbox(label=get_text('train_data_dir'), value=default_config["train_data_dir"], placeholder=get_text('train_data_dir_placeholder'))
            model_path = gr.Textbox(label=get_text('model_path'), value=default_config["model_path"], placeholder=get_text('model_path_placeholder'))
        with gr.Row():
            report_to = gr.Dropdown(label=get_text('report_to'), value=default_config["report_to"], choices=["all","wandb","tensorboard"])

    lora_accordion = gr.Accordion(get_text('lora_config'))
    with lora_accordion:
        # 训练相关设置
        with gr.Row():
            rank = gr.Number(label=get_text('rank'), value=default_config["rank"], info=get_text('rank_info'))
            train_batch_size = gr.Number(label=get_text('train_batch_size'), value=default_config["train_batch_size"], info=get_text('train_batch_size_info'))
        with gr.Row():
            repeats = gr.Number(label=get_text('repeats'), value=default_config["repeats"])
            gradient_accumulation_steps = gr.Number(label=get_text('gradient_accumulation_steps'), value=default_config["gradient_accumulation_steps"])
            mixed_precision = gr.Radio(label=get_text('mixed_precision'), value=default_config["mixed_precision"], choices=["bf16", "fp8"])
            gradient_checkpointing = gr.Checkbox(label=get_text('gradient_checkpointing'), value=default_config["gradient_checkpointing"])
        with gr.Row():
            optimizer = gr.Dropdown(label=get_text('optimizer'), value=default_config["optimizer"], choices=["adamw","prodigy"])
            lr_scheduler = gr.Dropdown(label=get_text('lr_scheduler'), value=default_config["lr_scheduler"], 
                        choices=["linear", "cosine", "cosine_with_restarts", "polynomial","constant", "constant_with_warmup"])
            cosine_restarts = gr.Number(label=get_text('cosine_restarts'), value=default_config["cosine_restarts"], info=get_text('cosine_restarts_info'), minimum=1)
        with gr.Row():
            learning_rate = gr.Number(label=get_text('learning_rate'), value=default_config["learning_rate"], info=get_text('learning_rate_info'))
            lr_warmup_steps = gr.Number(label=get_text('lr_warmup_steps'), value=default_config["lr_warmup_steps"])
            seed = gr.Number(label=get_text('seed'), value=default_config["seed"])
        with gr.Row():
            blocks_to_swap = gr.Number(label=get_text('blocks_to_swap'), value=default_config["blocks_to_swap"], info=get_text('blocks_to_swap_info'))
            mask_dropout = gr.Number(label=get_text('mask_dropout'), value=default_config["mask_dropout"], info=get_text('mask_dropout_info'))
            reg_ratio = gr.Number(label=get_text('reg_ratio'), value=default_config["reg_ratio"], info=get_text('reg_ratio_info'))
            reg_timestep = gr.Number(label=get_text('reg_timestep'), value=default_config["reg_timestep"], info=get_text('reg_timestep_info'))
            
            
    misc_accordion = gr.Accordion(get_text('misc'))
    with misc_accordion:
        with gr.Row():
            num_train_epochs = gr.Number(label=get_text('num_train_epochs'), value=default_config["num_train_epochs"], info=get_text('num_train_epochs_info'))
            save_model_epochs = gr.Number(label=get_text('save_model_epochs'), value=default_config["save_model_epochs"], info=get_text('save_model_epochs_info'))
            validation_epochs = gr.Number(label=get_text('validation_epochs'), value=default_config["validation_epochs"], info=get_text('validation_epochs_info'))
        with gr.Row():
            skip_epoch = gr.Number(label=get_text('skip_epoch'), value=default_config["skip_epoch"], info=get_text('skip_epoch_info'))
            skip_step = gr.Number(label=get_text('skip_step'), value=default_config["skip_step"], info=get_text('skip_step_info'))
            validation_ratio = gr.Number(label=get_text('validation_ratio'), value=default_config["validation_ratio"], info=get_text('validation_ratio_info'))
            
        with gr.Row():
            recreate_cache = gr.Checkbox(label=get_text('recreate_cache'), value=default_config["recreate_cache"])
            caption_dropout = gr.Number(label=get_text('caption_dropout'), value=default_config["caption_dropout"], info=get_text('caption_dropout_info'), maximum=1, minimum=0)
            max_time_steps = gr.Number(label=get_text('max_time_steps'), value=default_config["max_time_steps"], info=get_text('max_time_steps_info'), maximum=1000, minimum=0)
        
        resolution_md = gr.Markdown(get_text('resolution_section'))
        with gr.Row():
            resolution = gr.Dropdown(label=get_text('resolution'), value=default_config["resolution"], choices=default_config["resolution_choices"])
    
    misc_accordion = gr.Accordion(get_text('slider'))
    with misc_accordion:
        with gr.Row():
            use_two_captions = gr.Checkbox(label=get_text('use_two_captions'), value=default_config["use_two_captions"])
            slider_positive_scale = gr.Number(label=get_text('slider_positive_scale'), value=default_config["slider_positive_scale"])
            slider_negative_scale = gr.Number(label=get_text('slider_negative_scale'), value=default_config["slider_negative_scale"])
       
    
    
    # 输出和运行按钮
    output = gr.Textbox(label=get_text('output_box'))
    run_btn = gr.Button(get_text('run'))
    
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
        reg_timestep,
        use_two_captions,
        slider_positive_scale,
        slider_negative_scale
        # freeze_transformer_layers,
    ]
    
    # 语言切换处理函数
    def update_language_interface():
        """更新界面语言，返回所有需要更新的组件"""
        toggle_language()
        # 返回更新后的所有UI组件
        updated_components = [
            # 基础组件
            gr.Markdown(get_text('title')),  # 标题
            gr.Button(get_text('language_toggle'), scale=0, size="sm"),  # 语言切换按钮
            gr.Dropdown(label=get_text('script'), value=default_config["script"], choices=default_config["script_choices"]),  # 脚本选择
            gr.Textbox(scale=3, label=get_text('config_path'), value=default_config["config_path"], placeholder=get_text('config_path_placeholder')),  # 配置路径
            gr.Button(get_text('save'), scale=1),  # 保存按钮
            gr.Button(get_text('load'), scale=1),  # 加载按钮
            
            # Accordion组件更新
            gr.Accordion(get_text('directory_section')),  # 目录配置标题
            gr.Accordion(get_text('lora_config')),  # LoRA设置标题
            gr.Accordion(get_text('misc')),  # 杂项标题
            
            # 目录设置部分的组件
            gr.Textbox(label=get_text('output_dir'), value=default_config["output_dir"], placeholder=get_text('output_dir_placeholder')),  # 输出目录
            gr.Textbox(label=get_text('save_name'), value=default_config["save_name"], placeholder=get_text('save_name_placeholder')),  # 保存名称
            gr.Textbox(label=get_text('pretrained_model_name_or_path'), value=default_config["pretrained_model_name_or_path"], placeholder=get_text('pretrained_model_name_or_path_placeholder')),  # 预训练模型路径
            gr.Textbox(label=get_text('resume_from_checkpoint'), value=default_config["resume_from_checkpoint"], placeholder=get_text('resume_from_checkpoint_placeholder')),  # 恢复检查点
            gr.Textbox(label=get_text('train_data_dir'), value=default_config["train_data_dir"], placeholder=get_text('train_data_dir_placeholder')),  # 训练数据目录
            gr.Textbox(label=get_text('model_path'), value=default_config["model_path"], placeholder=get_text('model_path_placeholder')),  # 模型路径
            gr.Dropdown(label=get_text('report_to'), value=default_config["report_to"], choices=["all","wandb","tensorboard"]),  # 报告到
            
            # LoRA配置部分的组件
            gr.Number(label=get_text('rank'), value=default_config["rank"], info=get_text('rank_info')),  # 排名
            gr.Number(label=get_text('train_batch_size'), value=default_config["train_batch_size"], info=get_text('train_batch_size_info')),  # 训练批次大小
            gr.Number(label=get_text('repeats'), value=default_config["repeats"]),  # 重复次数
            gr.Number(label=get_text('gradient_accumulation_steps'), value=default_config["gradient_accumulation_steps"]),  # 梯度累积步数
            gr.Radio(label=get_text('mixed_precision'), value=default_config["mixed_precision"], choices=["bf16", "fp8"]),  # 混合精度
            gr.Checkbox(label=get_text('gradient_checkpointing'), value=default_config["gradient_checkpointing"]),  # 梯度检查点
            gr.Dropdown(label=get_text('optimizer'), value=default_config["optimizer"], choices=["adamw","prodigy"]),  # 优化器
            gr.Dropdown(label=get_text('lr_scheduler'), value=default_config["lr_scheduler"], choices=["linear", "cosine", "cosine_with_restarts", "polynomial","constant", "constant_with_warmup"]),  # 学习率调度器
            gr.Number(label=get_text('cosine_restarts'), value=default_config["cosine_restarts"], info=get_text('cosine_restarts_info'), minimum=1),  # 余弦重启
            gr.Number(label=get_text('learning_rate'), value=default_config["learning_rate"], info=get_text('learning_rate_info')),  # 学习率
            gr.Number(label=get_text('lr_warmup_steps'), value=default_config["lr_warmup_steps"]),  # 学习率预热步数
            gr.Number(label=get_text('seed'), value=default_config["seed"]),  # 随机种子
            gr.Number(label=get_text('blocks_to_swap'), value=default_config["blocks_to_swap"], info=get_text('blocks_to_swap_info')),  # 交换块数
            gr.Number(label=get_text('mask_dropout'), value=default_config["mask_dropout"], info=get_text('mask_dropout_info')),  # 掩码丢弃
            gr.Number(label=get_text('reg_ratio'), value=default_config["reg_ratio"], info=get_text('reg_ratio_info')),  # 正则化比率
            gr.Number(label=get_text('reg_timestep'), value=default_config["reg_timestep"], info=get_text('reg_timestep_info')),  # 正则化时间步
            
            # Misc部分的组件
            gr.Number(label=get_text('num_train_epochs'), value=default_config["num_train_epochs"], info=get_text('num_train_epochs_info')),  # 训练轮数
            gr.Number(label=get_text('save_model_epochs'), value=default_config["save_model_epochs"], info=get_text('save_model_epochs_info')),  # 保存模型轮数
            gr.Number(label=get_text('validation_epochs'), value=default_config["validation_epochs"], info=get_text('validation_epochs_info')),  # 验证轮数
            gr.Number(label=get_text('skip_epoch'), value=default_config["skip_epoch"], info=get_text('skip_epoch_info')),  # 跳过轮数
            gr.Number(label=get_text('skip_step'), value=default_config["skip_step"], info=get_text('skip_step_info')),  # 跳过步数
            gr.Number(label=get_text('validation_ratio'), value=default_config["validation_ratio"], info=get_text('validation_ratio_info')),  # 验证比率
            gr.Checkbox(label=get_text('recreate_cache'), value=default_config["recreate_cache"]),  # 重建缓存
            gr.Number(label=get_text('caption_dropout'), value=default_config["caption_dropout"], info=get_text('caption_dropout_info'), maximum=1, minimum=0),  # 标题丢弃
            gr.Number(label=get_text('max_time_steps'), value=default_config["max_time_steps"], info=get_text('max_time_steps_info'), maximum=1000, minimum=0),  # 最大时间步
            gr.Markdown(get_text('resolution_section')),  # 分辨率说明
            gr.Dropdown(label=get_text('resolution'), value=default_config["resolution"], choices=default_config["resolution_choices"]),  # 分辨率
            
            # 输出和运行按钮
            gr.Textbox(label=get_text('output_box')),  # 输出框
            gr.Button(get_text('run_button')),  # 运行按钮
            
            gr.Checkbox(label=get_text('use_two_captions'), value=default_config["use_two_captions"]),
            gr.Number(label=get_text('slider_positive_scale'), value=default_config["slider_positive_scale"]),
            gr.Number(label=get_text('slider_negative_scale'), value=default_config["slider_negative_scale"])
       
    
        ]
        return updated_components
    
    # 绑定事件处理器
    run_btn.click(fn=run, inputs=inputs, outputs=output, api_name="run")
    save_config_btn.click(fn=save_config, inputs=inputs)
    load_config_btn.click(fn=load_config, inputs=[config_path], outputs=inputs)
    
    # 语言切换事件处理 - 更新所有组件
    language_toggle_btn.click(
        fn=update_language_interface,
        inputs=[],
        outputs=[
            title_md, language_toggle_btn, script, config_path, save_config_btn, load_config_btn,
            directory_accordion, lora_accordion, misc_accordion,  # 添加Accordion组件
            output_dir, save_name, pretrained_model_name_or_path, resume_from_checkpoint, 
            train_data_dir, model_path, report_to,
            rank, train_batch_size, repeats, gradient_accumulation_steps, mixed_precision, gradient_checkpointing,
            optimizer, lr_scheduler, cosine_restarts, learning_rate, lr_warmup_steps, seed,
            blocks_to_swap, mask_dropout, reg_ratio, reg_timestep,
            num_train_epochs, save_model_epochs, validation_epochs, skip_epoch, skip_step, validation_ratio,
            recreate_cache, caption_dropout, max_time_steps, resolution_md, resolution,
            output, run_btn, 
            use_two_captions, slider_positive_scale,slider_negative_scale
        ]
    )

    # 添加数据集上传标签页
    add_dataset_upload_tab(demo)
    
# 启动界面
if __name__ == "__main__":
    demo.launch()