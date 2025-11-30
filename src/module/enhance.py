import numpy as np
import soundfile as sf
import torch
from denoiser import pretrained

class VoiceEnhancer:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.device)
        # 加载轻量化 denoiser
        self.model = pretrained.dns64().to(self.device)
        self.model.eval()

    def enhance(self, audio: np.ndarray, sr: int) -> np.ndarray:
        # 转成 tensor [batch, channels, samples]
        if audio.ndim == 1:
            audio_tensor = torch.from_numpy(audio).float().unsqueeze(0).unsqueeze(0)
        else:
            audio_tensor = torch.from_numpy(audio.T).float().unsqueeze(0)

        audio_tensor = audio_tensor.to(self.device)

        # 调用模型
        with torch.no_grad():
            enhanced = self.model(audio_tensor)

        # 取输出并转回 numpy
        enhanced = enhanced.squeeze().cpu().numpy()
        return enhanced

if __name__ == "__main__":
    input_path = "/Users/farshore/seven_project/vedio2voice/src/output/1764496910/0/0_1.wav"
    wav, sr = sf.read(input_path, always_2d=False)

    enhancer = VoiceEnhancer()
    enhanced = enhancer.enhance(wav, sr)

    sf.write("enhanced_denoiser.wav", enhanced, sr)
    print("💾 已输出增强音频：enhanced_denoiser.wav")
