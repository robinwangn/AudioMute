# -*- coding: utf-8 -*-
# 支持从 YAML 文件读取配置，实现灵活控制静音和音量百分比
# pycaw	控制 Windows 音频设备（静音、音量、设备切换）
# comtypes 与 Windows COM 接口交互，pycaw 的依赖
# PyYAML 用于解析你的 audio_config.yaml 配置文件
# 20250916 增加日志功能

import yaml
import os
import logging
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

def setup_logger():
    # 创建日志记录器
    logger = logging.getLogger('AudioManager')
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建文件处理器，将日志写入程序所在目录
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio_manager.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(file_handler)
    
    return logger

def load_config(config_path="audio_config.yaml"):
    logger = setup_logger()
    logger.info("程序启动，开始加载配置文件")
    
    if not os.path.exists(config_path):
        logger.error(f"配置文件未找到：{config_path}")
        print(f"⚠️ 配置文件未找到：{config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info("配置文件加载成功")
        return config
    except Exception as e:
        logger.error(f"配置文件加载失败：{str(e)}")
        print(f"❌ 配置文件加载失败：{str(e)}")
        return None

def apply_audio_policy(config):
    logger = setup_logger()
    logger.info("开始应用音频策略")
    
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        mute = config["audio"].get("mute")
        if mute is True:
            volume.SetMute(1, None)
            logger.info("设置音频设备为静音状态")
        elif mute is False:
            volume.SetMute(0, None)
            logger.info("设置音频设备为非静音状态")
        else:
            logger.info("未指定静音设置")

        vol = config["audio"].get("volume")
        if isinstance(vol, float) and 0.0 <= vol <= 1.0:
            volume.SetMasterVolumeLevelScalar(vol, None)
            logger.info(f"设置主音量为 {vol*100:.1f}%")
        elif vol is not None:
            logger.warning(f"音量值 {vol} 超出有效范围 (0.0-1.0)")
        else:
            logger.info("未指定音量设置")
            
        logger.info("音频策略应用完成")
    except Exception as e:
        logger.error(f"应用音频策略时发生错误：{str(e)}")
        print(f"❌ 应用音频策略时发生错误：{str(e)}")

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("音频管理程序开始运行")
    config = load_config()
    if config:
        apply_audio_policy(config)
        logger.info("音频管理程序执行完毕")
    else:
        logger.warning("由于配置加载失败，程序终止")