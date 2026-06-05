# AudioMute

Windows 音频自动管理工具 — 通过配置文件一键控制系统静音状态和音量大小，适合配合任务计划程序（Task Scheduler）实现定时静音。

## 功能特性

- ✅ 通过 YAML 配置文件控制系统静音（开/关）
- ✅ 设置系统主音量（0.0 ~ 1.0）
- ✅ 兼容直接运行 Python 脚本和 PyInstaller 打包后的 exe
- ✅ 自动记录日志到程序所在目录

## 快速开始

### 方式一：直接使用 exe（推荐，无需安装 Python）

1. 下载 `dist/` 目录下的 `audio_manager.exe` 和 `audio_config.yaml`
2. 将两个文件放在**同一目录**下
3. 编辑 `audio_config.yaml` 按需配置
4. 双击运行 `audio_manager.exe`，或通过 `run.bat` / 任务计划程序调用

### 方式二：运行 Python 脚本

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
2. 编辑 `audio_config.yaml`
3. 运行：
   ```
   python audio_manager.py
   ```

## 配置说明

编辑 `audio_config.yaml`：

```yaml
audio:
  mute: true         # 是否静音：true（静音）/ false（取消静音）
  volume: null       # 音量（0.0 ~ 1.0），null 表示不修改音量
```

**示例：静音并设置音量为 50%**
```yaml
audio:
  mute: true
  volume: 0.5
```

**示例：取消静音，音量不变**
```yaml
audio:
  mute: false
  volume: null
```

## 配合 Windows 任务计划程序使用

1. 打开"任务计划程序"（Task Scheduler）
2. 创建基本任务 → 设置触发时间（如每天 22:00）
3. 操作选择"启动程序"，选择 `audio_manager.exe` 或 `run.bat`
4. 确保 `audio_config.yaml` 与 exe 在同一目录

## 系统要求

- Windows 10 / 11
- （使用 exe 时无需其他依赖）
- （使用脚本时需 Python 3.8+）

## 依赖

| 包 | 用途 |
|----|------|
| pycaw | 控制 Windows 音频设备（静音、音量） |
| comtypes | Windows COM 接口交互（pycaw 依赖） |
| PyYAML | 解析 YAML 配置文件 |

## 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件
