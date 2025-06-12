# -*- coding: utf-8 -*-
"""
银河麒麟智能问答助手配置文件 - 基于SDK2.5更新
"""

import os
import platform

# DeepSeek-R1 API 配置
DEEPSEEK_API_KEY = "YOUR_API_KEY_HERE"
DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

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
    "language": "zh-CN",
    "rate": 150,
    "volume": 0.8,
    "voice_id": 0  # 语音ID
}

# GUI配置
GUI_CONFIG = {
    "window_title": "银河麒麟智能问答助手 v2.5",
    "window_size": "1000x750",
    "font_family": "SimHei",
    "font_size": 12,
    "theme": "default",  # 主题
    "icon_path": "./assets/icon.png"
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "./logs/app.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

# 向量数据库配置
VECTOR_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "similarity_threshold": 0.7,
    "max_results": 10
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
    "check_kylin_system": True,
    "enable_system_info": True,
    "enable_hardware_info": True,
    "enable_network_info": True,
    "auto_detect_encoding": True
}

# 安全配置
SECURITY_CONFIG = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "allowed_file_types": list(SUPPORTED_DOC_TYPES.keys()),
    "scan_uploads": True
}

# 性能配置
PERFORMANCE_CONFIG = {
    "max_concurrent_processes": 4,
    "cache_size": 100,
    "enable_gpu": False,
    "batch_size": 32
}

# 开发配置
DEVELOPMENT_CONFIG = {
    "debug_mode": False,
    "enable_profiling": False,
    "mock_api_calls": False
}

# 获取配置函数
def get_config(section: str = None):
    """
    获取配置信息
    """
    if section:
        return globals().get(f"{section.upper()}_CONFIG", {})
    else:
        return {
            "deepseek": {"api_key": DEEPSEEK_API_KEY, "endpoint": DEEPSEEK_API_ENDPOINT},
            "kylin_sdk": KYLIN_SDK_CONFIG,
            "vector": VECTOR_CONFIG,
            "rag": RAG_CONFIG,
            "gui": GUI_CONFIG,
            "log": LOG_CONFIG,
            "system": SYSTEM_CONFIG,
            "security": SECURITY_CONFIG,
            "performance": PERFORMANCE_CONFIG
        }

# 验证配置
def validate_config():
    """
    验证配置有效性
    """
    issues = []
    
    # 检查API密钥
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "YOUR_API_KEY_HERE":
        issues.append("DeepSeek API密钥未配置")
    
    # 检查必要目录
    for path in [DOCUMENT_PATH, os.path.dirname(VECTOR_DB_PATH), os.path.dirname(LOG_CONFIG['file'])]:
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                issues.append(f"无法创建目录 {path}: {str(e)}")
    
    return issues