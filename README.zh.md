# Video2Voice: 从视频到人声

[Switch to English version 切换到英文版](README.md)

## 项目概述
Video2Voice 是一个基于 Python 的工具，可实时处理音频以提取、增强语音片段并按说话人聚类。它结合了语音活动检测（VAD）、语音增强和说话人识别技术，提取音频中的说话人产生的语音。


## 核心功能
- **实时语音活动检测**：使用 Silero VAD 检测并提取语音片段。
- **语音增强**：提升语音片段的音频质量。
- **说话人识别**：使用 ECAPA-TDNN 嵌入按说话人聚类语音片段。
- **结构化输出**：按说话人 ID 保存组织好的语音片段。


## macOS 安装指南（系统音频捕获设置）

### 前置条件
1. **Homebrew**：安装 macOS 包管理器：  
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **PortAudio**：音频 I/O 必备：  
   ```bash
   brew install portaudio
   ```
3. **BlackHole 2ch**：用于捕获系统声音的虚拟音频环回设备：  
   ```bash
   brew install --cask blackhole-2ch
   ```

### 完整设置流程（系统音频捕获关键步骤）
按照以下步骤启用 Python 通过 BlackHole 2ch 捕获系统音频：  

#### 1. 创建多输出设备（推荐）  
   - 打开 **音频 MIDI 设置**（位于 `应用程序/实用工具` 或通过 Spotlight 搜索）。  
   - 点击左下角 `+` 按钮 → 选择 **创建多输出设备**。  
   - 在右侧面板勾选：  
     - 你的物理扬声器/耳机（如 "内建输出"）。  
     - `BlackHole 2ch`。  
   - 重命名设备（如 "BlackHole + 扬声器"）以便区分。  

#### 2. 配置系统音频输出  
   - 进入 **系统偏好设置 > 声音 > 输出**。  
   - 选择步骤 1 中创建的 `多输出设备`。  
   - *这样设置可确保音频同时通过扬声器和 BlackHole 播放（用于捕获）。*  

#### 3. 验证 Python 设备识别  
   - 运行以下测试脚本确认 BlackHole 已被检测：  
     ```python
     import sounddevice as sd
     print(sd.query_devices())  # 在列表中查找 "BlackHole 2ch"
     ```  

#### 4. 重启系统  
   - 安装 BlackHole 并创建多输出设备后，**重启 Mac** 以确保所有更改生效。  

#### 5. Python 环境设置  
   ```bash
   # 创建虚拟环境
   python3 -m venv video2voice
   source video2voice/bin/activate

   # 安装依赖
   pip install -r requirements.txt
   ```  


### 关键注意事项  
- **音频设备选择**：`src/main.py` 中的 `vad_device` 默认设置为 `"BlackHole 2ch"`。  
- **手动播放**：由于项目尚处于开发阶段，**建议手动播放和关闭目标视频切片**以确保稳定的音频捕获。  


## 项目状态  
⚠️ **开发预览版**：本项目处于活跃开发阶段。核心功能持续更新中。可通过 GitHub Issues 反馈问题。  


## 使用方法
1. **配置音频设备**：确保 `BlackHole 2ch` 已设为系统音频设备。
2. **运行 pipeline**：  
   ```bash
   cd src
   python main.py
   ```
3. **输出**：语音片段将保存至 `./output/<timestamp>/<speaker_id>/`，文件名如 `0_1.wav`。


## 使用的模型
### 1. Silero VAD（语音活动检测）
- **来源**：[snakers4/silero-vad](https://github.com/snakers4/silero-vad)
- **许可证**：MIT
- **用途**：实时检测语音片段。

### 2. SpeechBrain ECAPA-TDNN（说话人识别）
- **来源**：[speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)
- **许可证**：Apache-2.0
- **用途**：生成说话人嵌入以进行 diarization。

### 3. Facebook Denoiser（语音增强）
- **来源**：[facebookresearch/denoiser](https://github.com/facebookresearch/denoiser)
- **许可证**：MIT
- **用途**：降低背景噪声并提升语音质量。


## 输出结构
```
output/
└── <timestamp>/          # 唯一会话 ID
    └── <speaker_id>/     # 说话人聚类 ID
        ├── 0_1.wav       # 语音片段 1
        ├── 0_2.wav       # 语音片段 2
        ...
```


## 故障排除
- **音频设备未找到**：验证 BlackHole 是否已安装并在python中验证能回传系统的音频输出。
- **依赖冲突**：使用 `venv` 隔离环境。
- **语音检测准确率低**：调整 `vad.py` 中的 `speech_threshold`（默认值：0.8）。



## 许可证
MIT 许可证。详见 `LICENSE` 文件。
