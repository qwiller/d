# -*- coding: utf-8 -*-
"""
系统信息获取辅助模块 - 基于麒麟SDK2.5
"""

import ctypes
import logging
import os
import subprocess
from typing import Dict, Any, Optional
from config import KYLIN_SDK_CONFIG

class KylinSystemInfo:
    """
    麒麟系统信息获取类
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_kylin_libs()
    
    def _load_kylin_libs(self):
        """
        加载麒麟SDK库
        """
        try:
            # 根据SDK2.5文档加载相关库
            sdk_config = KYLIN_SDK_CONFIG
            
            # 检查库文件是否存在
            lib_paths = {
                'sysinfo': sdk_config.get('system_lib_path', '/usr/lib/aarch64-linux-gnu/libkysysinfo.so'),
                'hardware': sdk_config.get('hardware_lib_path', '/usr/lib/aarch64-linux-gnu/libkyhardware.so'),
                'time': sdk_config.get('time_lib_path', '/usr/lib/aarch64-linux-gnu/libkydate.so'),
                'package': sdk_config.get('package_lib_path', '/usr/lib/aarch64-linux-gnu/libkypackage.so')
            }
            
            self.libs = {}
            for lib_name, lib_path in lib_paths.items():
                if os.path.exists(lib_path):
                    try:
                        self.libs[lib_name] = ctypes.CDLL(lib_path)
                        self.logger.info(f"成功加载 {lib_name} 库: {lib_path}")
                    except Exception as e:
                        self.logger.warning(f"加载 {lib_name} 库失败: {str(e)}")
                        self.libs[lib_name] = None
                else:
                    self.logger.warning(f"{lib_name} 库文件不存在: {lib_path}")
                    self.libs[lib_name] = None
            
            # 设置函数原型
            self._setup_function_prototypes()
            
        except Exception as e:
            self.logger.error(f"加载麒麟SDK库失败: {str(e)}")
            self.libs = {}
    
    def _setup_function_prototypes(self):
        """
        设置C函数原型
        """
        try:
            if self.libs.get('sysinfo'):
                # 设置系统信息相关函数原型
                # 根据SDK2.5文档设置返回类型和参数类型
                lib = self.libs['sysinfo']
                
                # 字符串返回函数
                for func_name in ['kdk_system_get_architecture', 'kdk_system_get_systemName', 
                                'kdk_system_get_version', 'kdk_system_get_hostName']:
                    if hasattr(lib, func_name):
                        func = getattr(lib, func_name)
                        func.restype = ctypes.c_char_p
                        func.argtypes = []
                
                # 整数返回函数
                for func_name in ['kdk_system_get_word', 'kdk_system_get_buildTime']:
                    if hasattr(lib, func_name):
                        func = getattr(lib, func_name)
                        func.restype = ctypes.c_int
                        func.argtypes = []
                        
        except Exception as e:
            self.logger.error(f"设置函数原型失败: {str(e)}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        获取系统基础信息
        """
        info = {
            '操作系统': '银河麒麟',
            '获取时间': self._get_current_time()
        }
        
        # 使用SDK获取系统信息
        if self.libs.get('sysinfo'):
            info.update(self._get_sdk_system_info())
        
        # 使用系统命令获取补充信息
        info.update(self._get_system_command_info())
        
        return info
    
    def _get_sdk_system_info(self) -> Dict[str, Any]:
        """
        使用SDK获取系统信息
        """
        info = {}
        lib = self.libs['sysinfo']
        
        try:
            # 获取系统架构
            if hasattr(lib, 'kdk_system_get_architecture'):
                arch = lib.kdk_system_get_architecture()
                if arch:
                    info['系统架构'] = arch.decode('utf-8')
            
            # 获取系统名称
            if hasattr(lib, 'kdk_system_get_systemName'):
                name = lib.kdk_system_get_systemName()
                if name:
                    info['系统名称'] = name.decode('utf-8')
            
            # 获取系统版本
            if hasattr(lib, 'kdk_system_get_version'):
                version = lib.kdk_system_get_version()
                if version:
                    info['系统版本'] = version.decode('utf-8')
            
            # 获取主机名
            if hasattr(lib, 'kdk_system_get_hostName'):
                hostname = lib.kdk_system_get_hostName()
                if hostname:
                    info['主机名'] = hostname.decode('utf-8')
            
            # 获取系统位数
            if hasattr(lib, 'kdk_system_get_word'):
                word = lib.kdk_system_get_word()
                if word > 0:
                    info['系统位数'] = f"{word}位"
                    
        except Exception as e:
            self.logger.error(f"获取SDK系统信息失败: {str(e)}")
        
        return info
    
    def _get_system_command_info(self) -> Dict[str, Any]:
        """
        使用系统命令获取补充信息
        """
        info = {}
        
        try:
            # 获取内核版本
            result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
            if result.returncode == 0:
                info['内核版本'] = result.stdout.strip()
            
            # 获取CPU信息
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpu_info = f.read()
                    # 提取CPU型号
                    for line in cpu_info.split('\n'):
                        if 'model name' in line:
                            info['CPU型号'] = line.split(':')[1].strip()
                            break
                        elif 'Hardware' in line:  # ARM架构
                            info['硬件平台'] = line.split(':')[1].strip()
            except:
                pass
            
            # 获取内存信息
            try:
                with open('/proc/meminfo', 'r') as f:
                    mem_info = f.read()
                    for line in mem_info.split('\n'):
                        if 'MemTotal' in line:
                            mem_kb = int(line.split()[1])
                            mem_gb = round(mem_kb / 1024 / 1024, 2)
                            info['总内存'] = f"{mem_gb} GB"
                            break
            except:
                pass
            
            # 获取磁盘使用情况
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 4:
                        info['根分区大小'] = parts[1]
                        info['根分区已用'] = parts[2]
                        info['根分区可用'] = parts[3]
                        info['根分区使用率'] = parts[4]
            
            # 获取系统运行时间
            try:
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.read().split()[0])
                    days = int(uptime_seconds // 86400)
                    hours = int((uptime_seconds % 86400) // 3600)
                    minutes = int((uptime_seconds % 3600) // 60)
                    info['系统运行时间'] = f"{days}天 {hours}小时 {minutes}分钟"
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"获取系统命令信息失败: {str(e)}")
        
        return info
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """
        获取硬件信息
        """
        info = {}
        
        if self.libs.get('hardware'):
            info.update(self._get_sdk_hardware_info())
        
        # 补充系统命令获取的硬件信息
        info.update(self._get_command_hardware_info())
        
        return info
    
    def _get_sdk_hardware_info(self) -> Dict[str, Any]:
        """
        使用SDK获取硬件信息
        """
        info = {}
        # 这里可以根据SDK2.5文档添加具体的硬件信息获取函数调用
        return info
    
    def _get_command_hardware_info(self) -> Dict[str, Any]:
        """
        使用命令获取硬件信息
        """
        info = {}
        
        try:
            # 获取USB设备
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            if result.returncode == 0:
                usb_devices = len(result.stdout.strip().split('\n'))
                info['USB设备数量'] = usb_devices
            
            # 获取PCI设备
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            if result.returncode == 0:
                pci_devices = len(result.stdout.strip().split('\n'))
                info['PCI设备数量'] = pci_devices
                
        except Exception as e:
            self.logger.error(f"获取硬件信息失败: {str(e)}")
        
        return info
    
    def _get_current_time(self) -> str:
        """
        获取当前时间
        """
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        获取网络信息
        """
        info = {}
        
        try:
            # 获取网络接口信息
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            if result.returncode == 0:
                interfaces = []
                current_interface = None
                
                for line in result.stdout.split('\n'):
                    if ': ' in line and not line.startswith(' '):
                        if current_interface:
                            interfaces.append(current_interface)
                        current_interface = {'name': line.split(':')[1].strip().split('@')[0]}
                    elif 'inet ' in line and current_interface:
                        ip = line.strip().split()[1].split('/')[0]
                        current_interface['ip'] = ip
                
                if current_interface:
                    interfaces.append(current_interface)
                
                info['网络接口'] = interfaces
                
        except Exception as e:
            self.logger.error(f"获取网络信息失败: {str(e)}")
        
        return info
    
    def get_process_info(self) -> Dict[str, Any]:
        """
        获取进程信息
        """
        info = {}
        
        try:
            # 获取进程数量
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if result.returncode == 0:
                process_count = len(result.stdout.strip().split('\n')) - 1  # 减去标题行
                info['进程总数'] = process_count
            
            # 获取负载信息
            try:
                with open('/proc/loadavg', 'r') as f:
                    load_avg = f.read().strip().split()[:3]
                    info['系统负载'] = f"{load_avg[0]} {load_avg[1]} {load_avg[2]}"
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"获取进程信息失败: {str(e)}")
        
        return info
    
    def is_kylin_system(self) -> bool:
        """
        检查是否为麒麟系统
        """
        try:
            # 检查系统发行版信息
            release_files = ['/etc/kylin-release', '/etc/os-release']
            
            for file_path in release_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        content = f.read().lower()
                        if 'kylin' in content:
                            return True
            
            # 检查SDK库是否存在
            return any(lib is not None for lib in self.libs.values())
            
        except Exception as e:
            self.logger.error(f"检查系统类型失败: {str(e)}")
            return False
    
    def get_full_system_report(self) -> Dict[str, Any]:
        """
        获取完整的系统报告
        """
        report = {
            '基本信息': self.get_system_info(),
            '硬件信息': self.get_hardware_info(),
            '网络信息': self.get_network_info(),
            '进程信息': self.get_process_info(),
            '是否麒麟系统': self.is_kylin_system()
        }
        
        return report