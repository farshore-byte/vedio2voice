import threading
from module.vad import SystemVAD
from module.speaker import SpeakerRecognizer
from module.enhance import VoiceEnhancer
import os
import time

def vad_worker(vad, spk, enhancer):
    for clip in vad.start():  # 迭代器在后台线程运行
        print(f"⚡ 接收到一个语音片段，长度 {len(clip)/vad.SAMPLING_RATE:.2f} 秒")

        # --- 语音增强 ---
        enhanced_clip = enhancer.enhance(clip, vad.SAMPLING_RATE)

        # --- 说话人识别 ---
        spk_id, filepath = spk.recognize(enhanced_clip, vad.SAMPLING_RATE)
        print(f"🎤 语音片段归属说话人 {spk_id}, 保存: {filepath}")

def main():
    """
    语音处理管道主函数
    示例用法:
    1. 确保已安装 BlackHole 2ch 并设置为系统音频设备
    2. 运行命令: python src/main.py
    3. 播放包含语音的视频/音频文件
    4. 按 Ctrl+C 停止处理
    """
    vad_device = "BlackHole 2ch"  # macOS 推荐使用 BlackHole 2ch 捕获系统音频
    output_dir = "./output"       # 输出目录（自动创建）

    try:
        # 初始化组件
        vad = SystemVAD(device=vad_device)
        spk = SpeakerRecognizer(output_dir=output_dir)
        enhancer = VoiceEnhancer()  # 语音增强器（自动加载预训练模型）

        print("🟢 人声提取管道 启动 (按 Ctrl+C 停止)")
        print(f"📥 输出目录: {os.path.abspath(output_dir)}")

        # 启动处理线程
        t = threading.Thread(target=vad_worker, args=(vad, spk, enhancer), daemon=True)
        t.start()

        # 保持主进程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 退出监听模式")
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
