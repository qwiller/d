# 银河麒麟智能问答助手 v2.5

基于DeepSeek-R1 API和麒麟SDK2.5的智能问答系统，专为银河麒麟操作系统设计。

## 🌟 功能特性

- **智能问答**: 基于RAG(检索增强生成)技术，结合本地文档知识库和AI大模型
- **文档处理**: 支持PDF、Markdown、文本等多种格式文档
- **系统集成**: 深度集成麒麟SDK2.5，获取系统信息和硬件状态
- **图形界面**: 友好的GUI界面，支持文档管理和实时问答
- **多架构支持**: 支持x86_64和ARM64架构

## 📋 系统要求

### 推荐环境
- **操作系统**: 银河麒麟 V10 SP1/SP2/SP3
- **Python版本**: Python 3.7+
- **内存**: 4GB以上
- **存储**: 2GB可用空间

### 依赖库
- 麒麟SDK2.5开发库
- DeepSeek API访问权限
- Python第三方库（见requirements.txt）

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd kylin-qa-assistant