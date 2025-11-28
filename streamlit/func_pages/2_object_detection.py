import streamlit as st
import os
import sys
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import time  # 用于控制帧率
from docx import Document
from docx.shared import Inches
import serial  # 新增串口库

# 禁止 ultralytics 库检查或下载模型
os.environ['ULTRALYTICS_NO_CHECKS'] = '1'

# 禁止 ultralytics 库检查或下载模型
os.environ['ULTRALYTICS_NO_CHECKS'] = '1'

# 添加指定文件夹到系统路径
ultralytics_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ultralytics_dir)  # 插入到 sys.path 的最前面，确保优先加载

# 页面标题
st.title("🚀 火灾目标检测")

# 侧边栏：模型选择和输入方式
with st.sidebar:
    st.markdown("### 🛠️ 检测配置")

    # 模型文件列表
    weight_dir = os.path.join(os.path.dirname(__file__), "../..", "weight")  # weight 文件夹路径
    model_files = {
        "yolov8n": os.path.join(weight_dir, "yolov8n.pt"),
        "yolov8n_fire": os.path.join(weight_dir, "yolov8n-fire.pt"),
    }

    # 选择模型文件
    selected_model = st.selectbox("选择模型文件", list(model_files.keys()))

    def load_model(model_path):
        try:
            if not os.path.exists(model_path):  # 检查文件是否存在
                raise FileNotFoundError(f"模型文件不存在，请检查路径！")
            with st.spinner("正在加载模型..."):
                model = YOLO(model_path)  # 加载选择的模型
                st.success(f"模型加载成功！")
                return model
        except Exception as e:
            st.error(f"模型加载失败: {e}")
            return None


    model = load_model(model_files[selected_model])
    model_path = os.path.abspath(model_files[selected_model])

    # 只保留本地摄像头实时检测选项
    input_type = "本地摄像头实时检测"

    # 添加置信度滑块
    confidence_threshold = st.slider(
        "置信度阈值",
        min_value=0.0,
        max_value=1.0,
        value=0.25,  # 默认值
        step=0.01,
        help="调整置信度阈值以过滤检测结果。"
    )

# 初始化进度条
progress_bar = st.progress(0)

# 初始化串口（假设COM3，波特率9600，可根据实际情况修改）
try:
    arduino_serial = serial.Serial('COM3', 9600, timeout=1)
    arduino_serial.write(b'LED_OFF\n')  # 启动时确保LED关闭
    led_status = False
except Exception as e:
    arduino_serial = None
    led_status = False
    st.sidebar.warning(f"串口初始化失败: {e}")

# 只保留本地摄像头实时检测界面
st.markdown("### 📺 本地摄像头实时检测")

# 调用 utils.py 中的 infer_uploaded_webcam 进行实时检测
from streamlit.func_pages.utils import infer_uploaded_webcam

def arduino_led_controller():
    class Arduino:
        def __init__(self, serial_port, led_status):
            self.serial = serial_port
            self.led_status = led_status
    return Arduino(arduino_serial, led_status)

arduino = arduino_led_controller()
infer_uploaded_webcam(confidence_threshold, model, arduino)