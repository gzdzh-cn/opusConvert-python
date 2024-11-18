import os
import wave
import sys
from tqdm import tqdm
import opuslib
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("请提供输入文件路径作为命令行参数")
        return

    print("开始提取逻辑分析仪数据")

    # 获取输入文件名
    logic_name = sys.argv[1]
    logic_name_temp = logic_name.replace(".bin", "")
    logic_name_temp = logic_name_temp.split("\\")
    logic_name = logic_name_temp[-1]

    # 读取设置文件
    with open("opus_setting.txt", "r", errors="ignore") as set_file:
        setting_data = set_file.readlines()

    # 解析设置
    data = setting_data[1].strip().replace(" ", "").split(",")
    type1_channel = int(data[0])
    type1_framerate = int(data[1])
    type1_encframelen = int(data[2])
    type1_decframelen = int(data[3])
    type1_name = data[4]

    # 获取当前时间并格式化
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 去掉最后三位微秒，保留毫秒

    # 创建输出 WAV 文件
    output_filename = f"{timestamp}_{type1_name}.wav"
    output_type1_file = wave.open(output_filename, "wb")
    output_type1_file.setparams(
        (type1_channel, 2, type1_framerate, 0, "NONE", "not compressed")
    )

    print("从setting文件中,读取到的声道和采样率配置如下:")
    print(
        f"type1是 {type1_channel} 声道，采样率是 {type1_framerate} HZ，"
        f"编码帧长是 {type1_encframelen}，解码帧长是 {type1_decframelen}，"
        f"输出的文件名字是 {output_filename}"
    )

    # 打开二进制输入文件
    with open(logic_name + ".bin", "rb") as raw:
        size = os.path.getsize(logic_name + ".bin")
        progress_bar = tqdm(total=size, unit="B", unit_scale=True)

        # 初始化 Opus 解码器
        dec = opuslib.Decoder(fs=type1_framerate, channels=type1_channel)

        while True:
            raw_enc_data = raw.read(type1_encframelen)
            if len(raw_enc_data) < type1_encframelen:
                break

            # 解码数据
            try:
                decoded_data = dec.decode(raw_enc_data, type1_decframelen)
                output_type1_file.writeframes(decoded_data)
            except opuslib.OpusError as e:
                print(f"解码错误: {e}")
                break

            progress_bar.update(type1_encframelen)

        progress_bar.close()

    output_type1_file.close()
    print("处理完成")


if __name__ == "__main__":
    main()
