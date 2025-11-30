# Video2Voice: From video to Human voice

[Switch to Chinese version 切换到中文版](README.zh.md)

## Project Overview
Video2Voice is a Python-based tool that processes audio in real time to extract, enhance, and cluster speech segments by speaker. It combines speech activity detection (VAD), speech enhancement, and speaker recognition techniques to extract the speech produced by the speaker in the audio.


## Key Features
- **Real-Time VAD**: Detects and extracts speech segments using Silero VAD.
- **Voice Enhancement**: Improves audio quality of speech segments.
- **Speaker Diarization**: Clusters speech segments by speaker using ECAPA-TDNN embeddings.
- **Structured Output**: Saves organized speech segments by speaker ID.


## macOS Installation Guide (System Audio Capture Setup)

### Prerequisites
1. **Homebrew**: Install package manager for macOS:  
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **PortAudio**: Required for audio I/O:  
   ```bash
   brew install portaudio
   ```
3. **BlackHole 2ch**: Virtual audio loopback device for capturing system sound:  
   ```bash
   brew install --cask blackhole-2ch
   ```


### Complete Setup Flow (Critical for System Audio Capture)
Follow these steps to enable Python to capture system audio via BlackHole 2ch:  

#### 1. Create Multi-Output Device (Recommended)  
   - Open **Audio MIDI Setup** (found in `Applications/Utilities` or via Spotlight).  
   - Click the `+` button (bottom-left) → Select **Create Multi-Output Device**.  
   - In the right panel, check:  
     - Your physical speaker/headphone (e.g., "Built-in Output").  
     - `BlackHole 2ch`.  
   - Rename the device (e.g., "BlackHole + Speakers") for clarity.  

#### 2. Configure System Audio Output  
   - Go to **System Preferences > Sound > Output**.  
   - Select the `Multi-Output Device` created in Step 1.  
   - *This ensures audio plays through both your speakers and BlackHole (for capture).*  

#### 3. Verify Python Device Recognition  
   - Run this test script to confirm BlackHole is detected:  
     ```python
     import sounddevice as sd
     print(sd.query_devices())  # Look for "BlackHole 2ch" in the list
     ```  

#### 4. Restart Your System  
   - After installing BlackHole and creating the multi-output device, **restart your Mac** to ensure all changes take effect.  

#### 5. Python Environment Setup  
   ```bash
   # 创建虚拟环境
   python3 -m venv video2voice
   source video2voice/bin/activate

   # 安装依赖
   pip install -r requirements.txt
   ``` 

### Critical Notes  
- **Audio Device Selection**: The `vad_device` in `src/main.py` is set to `"BlackHole 2ch"` by default.  
- **Manual Playback**: Due to ongoing development, **manually play and close video files** to ensure stable audio capture.  


## Project Status  
⚠️ **Development Preview**: This project is in active development. Core features (VAD, enhancement, diarization) may have instability. Report issues via GitHub Issues.  


## Usage
1. **Configure Audio Device**: Ensure `BlackHole 2ch` is set as the system audio device.
2. **Run the Pipeline**:  
   ```bash
   cd src
   python main.py
   ```
3. **Output**: Speech segments are saved to `./output/<timestamp>/<speaker_id>/` with filenames like `0_1.wav`.


## Models Used
### 1. Silero VAD (Voice Activity Detection)
- **Source**: [snakers4/silero-vad](https://github.com/snakers4/silero-vad)
- **License**: MIT
- **Purpose**: Detects speech segments in real-time.

### 2. SpeechBrain ECAPA-TDNN (Speaker Recognition)
- **Source**: [speechbrain/spkrec-ecapa-voxceleb](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)
- **License**: Apache-2.0
- **Purpose**: Generates speaker embeddings for diarization.

### 3. Facebook Denoiser (Voice Enhancement)
- **Source**: [facebookresearch/denoiser](https://github.com/facebookresearch/denoiser)
- **License**: MIT
- **Purpose**: Reduces background noise and enhances speech quality.


## Output Structure
```
output/
└── <timestamp>/          # Unique session ID
    └── <speaker_id>/     # Speaker cluster ID
        ├── 0_1.wav       # Speech segment 1
        ├── 0_2.wav       # Speech segment 2
        ...
```


## Troubleshooting
- **Audio Device Not Found**: Verify BlackHole is installed and set as input/output in Sound Preferences.
- **Dependency Conflicts**: Use `venv` to isolate the environment.
- **Low Speech Detection Accuracy**: Adjust `speech_threshold` in `vad.py` (default: 0.8).


## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Submit a pull request with a detailed description of changes.


## License
MIT License. See `LICENSE` for details.
