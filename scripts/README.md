# 📜 Scripts 目录

本目录包含项目的各种运行和设置脚本，按操作系统分类。

## 🚀 运行脚本 (Run Scripts)

### Windows (.bat)
- `run.bat` - 启动 Flux Fill 界面
- `run_slider.bat` - 启动 Slider 界面
- `run_with_venv.bat` - 激活虚拟环境后启动 Kolors 界面
- `run_slider_with_venv.bat` - 激活虚拟环境后启动 Slider 界面

### Linux/macOS (.sh)
- `run.sh` - 启动 Flux Fill 界面
- `run_slider.sh` - 启动 Slider 界面
- `run_with_venv.sh` - 激活虚拟环境后启动 Kolors 界面
- `run_slider_with_venv.sh` - 激活虚拟环境后启动 Slider 界面

## ⚙️ 设置脚本 (Setup Scripts)

### Windows (.bat)
- `setup.bat` - Windows 环境自动配置脚本

### Linux/macOS (.sh)
- `setup.sh` - Linux/macOS 环境自动配置脚本

## 🎯 训练脚本 (Training Scripts)

### Linux/macOS (.sh)
- `train_kolors_lora_ui.sh` - Kolors LoRA 训练配置脚本

## 📋 使用方法

### 快速启动
```bash
# Windows
cd scripts
run.bat

# Linux/macOS
cd scripts
./run.sh
```

### 环境设置
```bash
# Windows
cd scripts
setup.bat

# Linux/macOS
cd scripts
chmod +x setup.sh
./setup.sh
```

### 训练
```bash
# Linux/macOS
cd scripts
chmod +x train_kolors_lora_ui.sh
./train_kolors_lora_ui.sh
```

## 🔧 注意事项

1. **权限设置**: Linux/macOS 脚本可能需要执行权限
2. **路径问题**: 脚本中的相对路径基于项目根目录
3. **虚拟环境**: 确保在正确的虚拟环境中运行脚本
4. **依赖检查**: 运行前请确保已安装所需依赖 