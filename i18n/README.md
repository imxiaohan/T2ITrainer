# 多语言国际化系统 (i18n)

这个目录包含了项目的多语言国际化支持系统。

## 文件结构

```
i18n/
├── __init__.py          # 包初始化文件，导出主要函数
├── translations.py      # 翻译字典和核心函数
└── README.md           # 本说明文件
```

## 使用方法

### 1. 导入翻译函数

```python
from i18n import get_text, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
```

### 2. 获取翻译文本

```python
# 获取默认语言的文本
text = get_text('title')

# 获取指定语言的文本
chinese_text = get_text('title', 'zh')
english_text = get_text('title', 'en')
```

### 3. 检查支持的语言

```python
# 获取支持的语言列表
languages = SUPPORTED_LANGUAGES  # ['zh', 'en']

# 检查是否为支持的语言
is_supported = is_supported_language('zh')  # True
```

## 添加新的翻译

### 1. 在 `translations.py` 中添加新的翻译键

```python
TRANSLATIONS = {
    'zh': {
        # ... 现有翻译
        'new_key': '新的中文翻译',
    },
    'en': {
        # ... 现有翻译
        'new_key': 'New English Translation',
    }
}
```

### 2. 在代码中使用

```python
new_text = get_text('new_key', current_language)
```

## 添加新的语言

### 1. 在 `translations.py` 中添加新语言

```python
TRANSLATIONS = {
    'zh': { ... },
    'en': { ... },
    'ja': {  # 新增日语
        'title': '## LoRA トレーニング',
        'script': 'トレーニングスクリプト',
        # ... 其他翻译
    }
}

# 更新支持的语言列表
SUPPORTED_LANGUAGES = ['zh', 'en', 'ja']
```

### 2. 更新默认语言（可选）

```python
DEFAULT_LANGUAGE = 'en'  # 或其他语言
```

## 特性

- **自动回退**: 如果请求的语言不存在，会自动回退到默认语言
- **键名回退**: 如果翻译键不存在，会返回键名本身
- **类型安全**: 支持的语言列表是只读的，避免意外修改
- **易于扩展**: 添加新语言或翻译键都很简单

## 测试

运行测试脚本验证系统：

```bash
python test_i18n.py
```

## 注意事项

1. 所有翻译键都应该在所有支持的语言中存在
2. 翻译文本应该保持一致的格式和风格
3. 新增翻译时记得同时更新所有语言版本
4. 建议使用有意义的键名，便于维护

## 在UI中的应用

在Gradio UI中，通常这样使用：

```python
# 创建组件时
button = gr.Button(get_text('run_button', current_language))

# 语言切换时
def update_language():
    global current_language
    current_language = 'en' if current_language == 'zh' else 'zh'
    return get_text('button_text', current_language)
``` 