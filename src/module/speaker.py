# 文件名: speaker_module.py
import os
import time
import numpy as np
import torch
import soundfile as sf
from speechbrain.pretrained import EncoderClassifier

class SpeakerRecognizer:
    """
    对语音片段进行声纹识别和聚类，并按说话人保存片段
    """
    def __init__(
        self,
        output_dir: str = "./output",
        similarity_threshold: float = 0.8,
        model_source: str = "speechbrain/spkrec-ecapa-voxceleb"
    ):
        self.base_dir = os.path.join(output_dir, f"{int(time.time())}")
        os.makedirs(self.base_dir, exist_ok=True)

        self.similarity_threshold = similarity_threshold
        self.classifier = EncoderClassifier.from_hparams(
            source=model_source,
            run_opts={"device": "cpu"}
        )

        self.speaker_embeddings = {}  # {speaker_id: embedding}
        self.speaker_counter = 0
        self.speaker_counters = {}   # {speaker_id: 当前片段序号}



    def recognize(self, audio_clip: np.ndarray, sampling_rate: int) -> tuple[int, str]:
        audio_clip = np.clip(audio_clip.astype(np.float32), -1.0, 1.0)
        print(audio_clip.shape)

        # 转 torch tensor 并加 batch 维度
        sig = torch.tensor(audio_clip).unsqueeze(0)  # [1, num_samples]

        # 获取 embedding
 
        output= self.classifier(sig)
        embedding = output[0].squeeze(0).cpu().numpy()  # 取 tuple 的第一个元素

        # 聚类逻辑
        for spk_id, spk_emb in self.speaker_embeddings.items():
            sim = np.dot(embedding, spk_emb) / (np.linalg.norm(embedding) * np.linalg.norm(spk_emb))
            if sim > self.similarity_threshold:
                folder = spk_id
                break
        else:
            folder = self.speaker_counter
            self.speaker_embeddings[folder] = embedding
            self.speaker_counter += 1
            os.makedirs(os.path.join(self.base_dir, str(folder)), exist_ok=True)
            self.speaker_counters[folder] = 0

        self.speaker_counters[folder] = self.speaker_counters.get(folder, 0) + 1
        file_idx = self.speaker_counters[folder]
        filename = os.path.join(self.base_dir, str(folder), f"{folder}_{file_idx}.wav")

        # 保存 wav 文件（可选）
        sf.write(filename, audio_clip, sampling_rate)

        return folder, filename


# ------------------- 测试 -------------------
if __name__ == "__main__":
    recognizer = SpeakerRecognizer(output_dir="output_test")
    dummy_clip = np.random.randn(16000).astype(np.float32) * 0.01
    spk_id, file_path = recognizer.recognize(dummy_clip, 16000)
    print(f"语音片段属于说话人 {spk_id}, 已保存到 {file_path}")
