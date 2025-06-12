# -*- coding: utf-8 -*-
"""
AI模型接口模块 - 硅基流动API集成
"""

import requests
import json
import logging
from typing import List, Dict, Any, Optional
from config import SILICONFLOW_API_KEY, SILICONFLOW_API_ENDPOINT, RAG_CONFIG

class SiliconFlowAPI:
    """
    硅基流动API接口类
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or SILICONFLOW_API_KEY
        self.endpoint = SILICONFLOW_API_ENDPOINT
        self.logger = logging.getLogger(__name__)
        
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            self.logger.warning("硅基流动API密钥未配置")
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                       model: str = "Qwen/Qwen2.5-72B-Instruct",
                       temperature: float = 0.7,
                       max_tokens: int = 1000,
                       stream: bool = False) -> Dict[str, Any]:
        """
        调用硅基流动聊天完成API
        
        Args:
            messages: 对话消息列表
            model: 模型名称，默认使用Qwen2.5-72B-Instruct
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否流式输出
            
        Returns:
            API响应结果
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': stream
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"硅基流动API调用失败: {e}")
            return {"error": str(e)}
    
    def generate_answer(self, question: str, context: str = "", 
                       include_system_info: bool = False,
                       system_info: str = "") -> str:
        """
        生成问答回复
        
        Args:
            question: 用户问题
            context: 相关文档上下文
            include_system_info: 是否包含系统信息
            system_info: 系统信息
            
        Returns:
            AI生成的回答
        """
        # 构建系统提示词
        system_prompt = """
你是银河麒麟操作系统的智能助手，专门帮助用户解答关于麒麟系统的问题。
请基于提供的文档内容和系统信息，给出准确、有用的回答。
如果问题超出了提供的信息范围，请诚实地说明。
        """.strip()
        
        # 构建用户消息
        user_message = f"问题：{question}"
        
        if context:
            user_message += f"\n\n相关文档：\n{context}"
        
        if include_system_info and system_info:
            user_message += f"\n\n当前系统信息：\n{system_info}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # 调用API
        response = self.chat_completion(
            messages=messages,
            temperature=RAG_CONFIG.get('temperature', 0.7),
            max_tokens=RAG_CONFIG.get('max_tokens', 1000)
        )
        
        if "error" in response:
            return f"抱歉，生成回答时出现错误：{response['error']}"
        
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            self.logger.error(f"解析API响应失败: {e}")
            return "抱歉，无法解析AI回答，请稍后重试。"
    
    def get_available_models(self) -> List[str]:
        """
        获取可用的模型列表
        
        Returns:
            可用模型列表
        """
        # 硅基流动支持的主要模型
        return [
            "Qwen/Qwen2.5-72B-Instruct",
            "Qwen/Qwen2.5-32B-Instruct", 
            "Qwen/Qwen2.5-14B-Instruct",
            "Qwen/Qwen2.5-7B-Instruct",
            "Pro/deepseek-ai/DeepSeek-R1",
            "deepseek-ai/DeepSeek-V3",
            "01-ai/Yi-1.5-34B-Chat",
            "meta-llama/Llama-3.1-70B-Instruct",
            "meta-llama/Llama-3.1-8B-Instruct",
            "THUDM/glm-4-9b-chat"
        ]
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            连接是否成功
        """
        test_messages = [
            {"role": "user", "content": "你好"}
        ]
        
        response = self.chat_completion(
            messages=test_messages,
            max_tokens=10
        )
        
        return "error" not in response