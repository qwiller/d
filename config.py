# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手配置文件 - 基于硅基流动API和麒麟SDK2.5
"""

import os
import platform

# 应用版本信息
APP_VERSION = "2.6.0"
APP_NAME = "银河麒麟智能问答助手"
APP_DESCRIPTION = "基于硅基流动API和麒麟SDK2.5的智能问答系统"

# 硅基流动 API 配置
SILICONFLOW_API_KEY = "YOUR_API_KEY_HERE"
SILICONFLOW_API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"

# 文档路径配置
DOCUMENT_PATH = "./docs"
VECTOR_DB_PATH = "./data/vector_db"

# 检测系统架构
ARCH = platform.machine().lower()
if ARCH in ['aarch64', 'arm64']:
    LIB_ARCH = "aarch64-linux-gnu"
elif ARCH in ['x86_64', 'amd64']:
    LIB_ARCH = "x86_64-linux-gnu"
else:
    LIB_ARCH = "linux-gnu"

# 麒麟SDK2.5配置
KYLIN_SDK_CONFIG = {
    "version": "2.5",
    "system_lib_path": f"/usr/lib/{LIB_ARCH}/libkysysinfo.so",
    "hardware_lib_path": f"/usr/lib/{LIB_ARCH}/libkyhardware.so",
    "time_lib_path": f"/usr/lib/{LIB_ARCH}/libkydate.so",
    "package_lib_path": f"/usr/lib/{LIB_ARCH}/libkypackage.so",
    "fallback_paths": [
        "/usr/lib/libkysysinfo.so",
        "/usr/local/lib/libkysysinfo.so",
        "./lib/libkysysinfo.so"
    ]
}

# 支持的文档类型（基于SDK2.5文档格式）
SUPPORTED_DOC_TYPES = {
    '.pdf': 'PDF文档',
    '.md': 'Markdown文档', 
    '.txt': '文本文档',
    '.rst': 'reStructuredText文档',
    '.doc': 'Word文档',
    '.docx': 'Word文档',
    '.html': 'HTML文档',
    '.htm': 'HTML文档'
}

# 语音配置
VOICE_CONFIG = {
    "recognition_language": "zh-CN",
    "speech_rate": 150,
    "speech_volume": 0.8,
    "timeout": 5,
    "phrase_timeout": 1
}

# GUI配置
GUI_CONFIG = {
    "window_title": "银河麒麟智能问答助手 v2.6.0",
    "window_size": "1200x800",
    "theme": "default"
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "file": "./logs/app.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# 向量数据库配置
VECTOR_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "embedding_model": "text-embedding-ada-002"
}

# RAG配置
RAG_CONFIG = {
    "top_k": 5,
    "similarity_threshold": 0.7,
    "max_context_length": 2000,
    "temperature": 0.7,
    "max_tokens": 1000
}

# 系统配置
SYSTEM_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "supported_languages": ["zh-CN", "en-US"]
}

# 安全配置
SECURITY_CONFIG = {
    "api_timeout": 30,
    "max_retries": 3
}

# 性能配置
PERFORMANCE_CONFIG = {
    "max_concurrent_processes": 4,
    "cache_size": 100,
    "batch_size": 32
}

# 开发配置
DEV_CONFIG = {
    "debug": False,
    "log_api_calls": False
}

# API配置映射
API_CONFIGS = {
    "siliconflow": {"api_key": SILICONFLOW_API_KEY, "endpoint": SILICONFLOW_API_ENDPOINT},
}

def get_config(key, default=None):
    """获取配置值"""
    return globals().get(key, default)

def validate_config():
    """验证配置"""
    issues = []
    
    if not SILICONFLOW_API_KEY or SILICONFLOW_API_KEY == "YOUR_API_KEY_HERE":
        issues.append("硅基流动API密钥未配置")
    
    if not os.path.exists(DOCUMENT_PATH):
        issues.append(f"文档路径不存在: {DOCUMENT_PATH}")
    
    return issues