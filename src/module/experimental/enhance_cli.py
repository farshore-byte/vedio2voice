import subprocess
import os

def enhance_audio(input_path, output_dir="output", model="htdemucs", device="cuda"):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "demucs", input_path,
        "-n", model,
        "-o", output_dir
    ]
    subprocess.run(cmd, check=True)
    # 增强后的文件在 output/<model>/<filename> 下
    base_name = os.path.basename(input_path)
    enhanced_path = os.path.join(output_dir, model, base_name)
    return enhanced_path

if __name__ == "__main__":
    input_wav = "/Users/farshore/seven_project/vedio2voice/src/output/1764496910/0/0_1.wav"
    enhanced_path = enhance_audio(input_wav)
    print("增强完成，保存路径:", enhanced_path)