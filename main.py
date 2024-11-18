import os
import wave
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tqdm import tqdm
import opuslib
from datetime import datetime

app = FastAPI()

class ConvertRequest(BaseModel):
    input_file: str
    output_path: str


@app.post("/binTranWav")
async def binTranWav(request: ConvertRequest):
    input_file = request.input_file
    output_path = request.output_path

    if not input_file or not output_path:
        raise HTTPException(status_code=400, detail="请提供输入文件路径和输出路径")

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
        type1_channel = int(data[0])  # 1
        type1_framerate = int(data[1])  # 16000
        type1_encframelen = int(data[2])  # 40
        type1_decframelen = int(data[3])  # 320
        type1_name = data[4]  # opus_dec

        # 获取当前时间并格式化
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # 去掉最后三位微秒，保留毫秒

        # 创建输出 WAV 文件
        output_filename = os.path.join(output_path, f"{timestamp}_{type1_name}.wav")
        print("output_filename:", output_filename)
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
                    raise HTTPException(status_code=500, detail=f"解码错误: {e}")
                progress_bar.update(type1_encframelen)

            progress_bar.close()

        output_type1_file.close()
        output_file = os.path.join("/", f"{timestamp}_{type1_name}.wav")
        return {"message": "处理完成", "output_file": output_file}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
