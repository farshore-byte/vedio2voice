# 文件名: vad_module.py
import torch
import numpy as np
import sounddevice as sd
import datetime
import time
import os
import torchaudio
from collections import deque

class SystemVAD:
    def __init__(self, device: str = None, speech_threshold: float = 0.80, save_dir: str = None):
        self.device = device
        self.SAMPLING_RATE = 16000
        self.window_size_samples = 512
        self.speech_threshold = speech_threshold
        self.max_silence_duration = 2.0  # 最大静音时长（秒）
        self.save_dir = save_dir
        if self.save_dir:
            os.makedirs(self.save_dir, exist_ok=True)

        self.pre_chunks = deque(maxlen=30)
        self.max_post_chunks = 30
        self.post_chunks_nums = self.max_post_chunks

        # 加载 Silero VAD
        self.model, _ = torch.hub.load('snakers4/silero-vad', 'silero_vad', force_reload=False)

        # 状态变量
        self.speech_wav = np.array([])
        self.delay_time = 0.0
        self.activate = False
        self.counter = 0
        self._queue = []

    @staticmethod
    def timestamp():
        return datetime.datetime.now().strftime("[%H:%M:%S]")

    def _print_progress(self, prefix, value, max_value, seconds):
        """单行显示进度条"""
        BAR_WIDTH = 20
        filled = min(BAR_WIDTH, int(value / max_value * BAR_WIDTH))
        bar = "█" * filled + "-" * (BAR_WIDTH - filled)
        print(f"\r{prefix} [{bar}] {seconds:.2f}s", end="", flush=True)

    def _callback(self, indata, frames, time_info, status):
        chunk = indata.mean(axis=1).astype(np.float32)
        if len(chunk) < self.window_size_samples:
            chunk = np.pad(chunk, (0, self.window_size_samples - len(chunk)))

        speech_prob = self.model(torch.from_numpy(chunk), self.SAMPLING_RATE).item()
        self.counter += 1
        self.pre_chunks.append(chunk)

        if speech_prob > self.speech_threshold:
            if not self.activate:
                print(f"\n{self.timestamp()} 🎙️ 检测到人声")
                self.speech_wav = np.concatenate(list(self.pre_chunks))
            self.activate = True
            self.delay_time = 0.0
            self.speech_wav = np.concatenate((self.speech_wav, chunk))
            self.post_chunks_nums = 0
            # 讲话进度条
            self._print_progress("🎤 讲话中", len(self.speech_wav)/self.SAMPLING_RATE, 2.0, len(self.speech_wav)/self.SAMPLING_RATE)
        else:
            if self.activate:
                self.delay_time += self.window_size_samples / self.SAMPLING_RATE
                if self.post_chunks_nums < self.max_post_chunks:
                    self.speech_wav = np.concatenate((self.speech_wav, chunk))
                    self.post_chunks_nums += 1
                else:
                    self.speech_wav = np.concatenate((self.speech_wav, np.zeros_like(chunk)))
                # 静音进度条
                self._print_progress("😴 静音中", self.delay_time, self.max_silence_duration, self.delay_time)

                if self.delay_time >= self.max_silence_duration:
                    duration = len(self.speech_wav)/self.SAMPLING_RATE
                    print(f"\n{self.timestamp()} ✅ 讲话结束 | 总时长：{duration:.2f}s")
                    if self.save_dir:
                        filename = os.path.join(self.save_dir, f"vad_{int(time.time())}.wav")
                        torchaudio.save(torch.from_numpy(self.speech_wav).unsqueeze(0),
                                        filename, self.SAMPLING_RATE)
                        print(f"💾 已保存: {filename}")
                    self._queue.append(self.speech_wav.copy())
                    self.speech_wav = np.array([])
                    self.activate = False
                    self.delay_time = 0.0
                    self.pre_chunks.clear()
                    self.post_chunks_nums = self.max_post_chunks

    def start(self):
        print("🎤 语音活动检测已启动...\n")
        try:
            with sd.InputStream(
                device=self.device,
                channels=2,
                samplerate=self.SAMPLING_RATE,
                blocksize=self.window_size_samples,
                callback=self._callback
            ):
                print(f"🎧 正在监听系统音频... 按 Ctrl+C 退出")
                while True:
                    if self._queue:
                        yield self._queue.pop(0)
                    time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n👋 已手动退出监听模式")


# ------------------- 测试 -------------------
if __name__ == "__main__":
    vad = SystemVAD(device=None, save_dir="vad_clips")
    for clip in vad.start():
        print(f"\n⚡ 收到一个语音片段，长度 {len(clip)/vad.SAMPLING_RATE:.2f} 秒")
