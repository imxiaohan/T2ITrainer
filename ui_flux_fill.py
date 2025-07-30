import gradio as gr

import subprocess
import json
import sys
import os
from dataset_upload import add_dataset_upload_tab

# ===== 语言翻译系统 =====
sys.path.append('i18n')
from translator import translator
def get_text(key):
    """获取当前语言的文本（兼容性包装器）"""
    return translator.get_text(key)

def toggle_language():
    """切换语言（兼容性包装器）"""
    return translator.toggle_language()

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