# -*- coding: utf-8 -*-
"""
多语言国际化包
"""

from .translations import (
    TRANSLATIONS,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    get_text,
    get_supported_languages,
    is_supported_language
)

__all__ = [
    'TRANSLATIONS',
    'SUPPORTED_LANGUAGES', 
    'DEFAULT_LANGUAGE',
    'get_text',
    'get_supported_languages',
    'is_supported_language'
]

# 确保这些变量可以直接从包中访问
__version__ = '1.0.0' 