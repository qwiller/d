# -*- coding: utf-8 -*-
"""
AI模型接口模块 - DeepSeek-R1 API集成
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_ENDPOINT, RAG_CONFIG

class DeepSeekAPI:
    """
    DeepSeek-R1 API接口类
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.endpoint = DEEPSEEK_API_ENDPOINT
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            self.logger.warning("DeepSeek API密钥未配置")
    
    def generate_response(self, messages: List[Dict[str, str]], 
                         temperature: float = None,
                         max_tokens: int = None) -> Optional[str]:
        """
        生成AI响应
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            AI生成的响应文本
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-reasoner',
                'messages': messages,
                'temperature': temperature or RAG_CONFIG.get('temperature', 0.7),
                'max_tokens': max_tokens or RAG_CONFIG.get('max_tokens', 1000),
                'stream': False
            }
            
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                self.logger.error(f"API请求失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"生成响应失败: {str(e)}")
            return None
    
    def build_system_prompt(self, context: str = "") -> str:
        """
        构建系统提示词
        
        Args:
            context: 上下文信息
            
        Returns:
            系统提示词
        """
        base_prompt = """
你是银河麒麟操作系统的智能问答助手，专门帮助用户解决麒麟系统相关的问题。

你的能力包括：
1. 回答银河麒麟系统的使用问题
2. 提供系统配置和故障排除建议
3. 解释麒麟SDK2.5的接口和功能
4. 协助进行系统管理和维护

回答要求：
- 使用中文回答
- 提供准确、实用的信息
- 如果不确定，请明确说明
- 优先使用提供的上下文信息
"""
        
        if context:
            base_prompt += f"\n\n相关文档内容：\n{context}"
        
        return base_prompt
    
    def answer_question(self, question: str, context: str = "") -> Optional[str]:
        """
        回答用户问题
        
        Args:
            question: 用户问题
            context: 相关上下文
            
        Returns:
            AI回答
        """
        messages = [
            {
                "role": "system",
                "content": self.build_system_prompt(context)
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        return self.generate_response(messages)