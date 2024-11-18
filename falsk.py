import os
import wave
from flask import Flask, request, jsonify
from tqdm import tqdm
import opuslib

app = Flask(__name__)


@app.route('/binTranWav', methods=['POST'])
def binTranWav():
    data = request.json
    input_file = data.get('input_file')
    output_path = data.get('output_path')

    if not input_file or not output_path:
        return jsonify({"error": "请提供输入文件路径和输出路径"}), 400

    try:
        # 获取输入文件名
        logic_name_temp = input_file.replace(".bin", "")
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

        # 创建输出 WAV 文件
        output_filename = os.path.join(output_path, f"{logic_name}_output_{type1_name}.wav")
        output_type1_file = wave.open(output_filename, "wb")
        output_type1_file.setparams(
            (type1_channel, 2, type1_framerate, 0, "NONE", "not compressed")
        )

        # 打开二进制输入文件
        with open(input_file, "rb") as raw:
            size = os.path.getsize(input_file)
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
                    return jsonify({"error": f"解码错误: {e}"}), 500

                progress_bar.update(type1_encframelen)

            progress_bar.close()

        output_type1_file.close()
        return jsonify({"message": "处理完成", "output_file": output_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
