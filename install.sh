#!/bin/bash

# 银河麒麟智能问答助手安装脚本

set -e

echo "银河麒麟智能问答助手安装程序"
echo "========================================"

# 检查权限
if [ "$EUID" -ne 0 ]; then
    echo "请使用sudo运行此安装脚本"
    exit 1
fi

# 检查系统
if [ ! -f "/etc/kylin-release" ] && ! grep -q "Kylin" /etc/os-release 2>/dev/null; then
    echo "警告: 此程序专为银河麒麟系统设计"
    read -p "是否继续安装? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 安装目录
INSTALL_DIR="/opt/kylin-qa-assistant"
echo "安装目录: $INSTALL_DIR"

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 复制文件
echo "复制程序文件..."
cp -r * "$INSTALL_DIR/"

# 设置权限
chown -R kylin:kylin "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/run.sh"
chmod +x "$INSTALL_DIR/main.py"

# 安装Python依赖
echo "安装Python依赖..."
cd "$INSTALL_DIR"
pip3 install -r requirements.txt

# 创建数据目录
mkdir -p "$INSTALL_DIR/data" "$INSTALL_DIR/logs" "$INSTALL_DIR/docs"
chown -R kylin:kylin "$INSTALL_DIR/data" "$INSTALL_DIR/logs" "$INSTALL_DIR/docs"

# 安装系统服务
echo "安装系统服务..."
cp kylin-qa.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable kylin-qa.service

# 创建桌面快捷方式
echo "创建桌面快捷方式..."
cat > /home/kylin/Desktop/kylin-qa.desktop << EOF
[Desktop Entry]
Version=2.6.0
Type=Application
Name=银河麒麟智能问答助手
Comment=基于AI的银河麒麟系统智能问答助手
Exec=$INSTALL_DIR/run.sh
Icon=$INSTALL_DIR/icon.png
Terminal=false
Categories=Utility;System;
EOF

chown kylin:kylin /home/kylin/Desktop/kylin-qa.desktop
chmod +x /home/kylin/Desktop/kylin-qa.desktop

# 创建命令行快捷方式
ln -sf "$INSTALL_DIR/run.sh" /usr/local/bin/kylin-qa

echo "安装完成！"
echo ""
echo "使用方法:"
echo "1. 图形界面: 双击桌面上的'银河麒麟智能问答助手'图标"
echo "2. 命令行: 运行 'kylin-qa' 命令"
echo "3. 系统服务: systemctl start kylin-qa"
echo ""
echo "配置文件位置: $INSTALL_DIR/config.py"
echo "日志文件位置: $INSTALL_DIR/logs/app.log"
echo ""
echo "请在使用前配置DeepSeek API密钥！"