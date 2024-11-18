# opus转换
python 3.11

> opus转换常用格式音频

### 更新日志
v1.0.0 -日期：2024-11-18
- 二进制文件转换为 WAV 格式


## 接口方式运行
```shell
uvicorn main:app --reload

```
## 接口文档

此接口用于将输入的二进制文件转换为 WAV 格式。

### URL

`POST http://127.0.0.1:8000/tranWav`

### 请求

#### 请求头

- `Content-Type: application/json`

#### 请求体参数

- `input_file` (字符串): 需要转换的 `.bin` 输入文件的路径。
- `output_path` (字符串): 保存输出 WAV 文件的目录。

##### 示例

```json
{
    "input_file": "/Users/lizheng/Downloads/音频/tranwav/input.bin",
    "output_path": "./"
}
```

### 响应
#### 成功 (200 OK)
* message (字符串): 表示处理成功的确认信息。
* output_file (字符串): 生成的 WAV 文件的路径。

##### 示例
```shell
{
    "message": "处理完成",
    "output_file": "./input_20241116032900_output.wav"
}

```


## exe方式运行本地测试
```shell
python exe.py input.bin

```