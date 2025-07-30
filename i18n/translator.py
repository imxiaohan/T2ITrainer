import json
import os
from typing import Dict, Any

class Translator:
    """国际化翻译器类"""
    
    def __init__(self, languages_dir: str = "i18n"):
        self.languages_dir = languages_dir
        self.current_language = "en"
        self.translations: Dict[str, Dict[str, str]] = {}
        self.supported_languages = ["en", "zh"]
        self.load_languages()
    
    def load_languages(self):
        """加载所有支持的语言文件"""
        for lang in self.supported_languages:
            lang_file = os.path.join(self.languages_dir, f"{lang}.json")
            if os.path.exists(lang_file):
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                except Exception as e:
                    print(f"Error loading language file {lang_file}: {e}")
                    self.translations[lang] = {}
            else:
                print(f"Language file not found: {lang_file}")
                self.translations[lang] = {}
    
    def set_language(self, language: str):
        """设置当前语言"""
        if language in self.supported_languages:
            self.current_language = language
        else:
            print(f"Unsupported language: {language}")
    
    def get_text(self, key: str, default: str = None) -> str:
        """获取翻译文本"""
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, default or key)
        return default or key
    
    def toggle_language(self) -> str:
        """切换语言"""
        self.current_language = "zh" if self.current_language == "en" else "en"
        return self.current_language
    
    def get_available_languages(self) -> list:
        """获取可用语言列表"""
        return self.supported_languages
    
    def reload_translations(self):
        """重新加载所有语言文件（用于开发调试）"""
        self.translations.clear()
        self.load_languages()

# 创建全局翻译器实例
translator = Translator()