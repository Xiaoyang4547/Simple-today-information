from datetime import datetime#导入时间模块
from easygui import *
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QDateTime

#Simple today's information是一个简单的今日信息查询程序
msgbox("欢迎使用Simple today's information!",'启动程序',ok_button='继续')
def get_weather(city="桂林七星"):
    # 你的和风天气KEY
    key = "c5dada73c55d40cd962c9f6299d83496"  # ← 请替换为你自己的KEY
    # 获取城市的location ID（这里以北京为例，实际可用API查询城市ID）
    location = "101020100"  # 北京的location ID，可根据需要更换
    try:
        url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={key}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "200":
                now = data["now"]
                text = now["text"]
                temp = now["temp"]
                return f"{city}天气：{text}，{temp}℃"
            else:
                return f"天气获取失败，错误码：{data.get('code')}"
        else:
            return "天气获取失败"
    except Exception as e:
        return f"天气获取异常: {e}"

class TimeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("当前时间与天气显示")
        self.resize(350, 150)
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.weather_label = QLabel()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.weather_label)
        self.setLayout(self.layout)

        # 定时器每秒更新一次时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # 启动时获取一次天气
        self.update_weather()

    def update_time(self):
        now = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.label.setText(f"当前时间：{now}")

    def update_weather(self):
        weather = get_weather("北京")  # 你可以改成其他城市
        self.weather_label.setText(f"当前天气：{weather}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeWindow()
    window.show()
    sys.exit(app.exec_())