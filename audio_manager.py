# -*- coding: utf-8 -*-
# 支持从 YAML 文件读取配置，实现灵活控制静音和音量百分比

# pycaw	控制 Windows 音频设备（静音、音量、设备切换）
# comtypes 与 Windows COM 接口交互，pycaw 的依赖
# PyYAML 用于解析你的 audio_config.yaml 配置文件

import yaml
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

def load_config(config_path="audio_config.yaml"):
    if not os.path.exists(config_path):
        print(f"⚠️ 配置文件未找到：{config_path}")
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def apply_audio_policy(config):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    mute = config["audio"].get("mute")
    if mute is True:
        volume.SetMute(1, None)
    elif mute is False:
        volume.SetMute(0, None)

    vol = config["audio"].get("volume")
    if isinstance(vol, float) and 0.0 <= vol <= 1.0:
        volume.SetMasterVolumeLevelScalar(vol, None)

if __name__ == "__main__":
    config = load_config()
    if config:
        apply_audio_policy(config)
