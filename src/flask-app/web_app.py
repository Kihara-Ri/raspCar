from flask import Flask, Response, render_template
import cv2
import time

app = Flask(__name__)

# 打开摄像头捕获
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("摄像头未能成功开启")
    exit()
    
CAP_WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
CAP_HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Caption画面分辨率: {CAP_WIDTH} x {CAP_HEIGHT}") # 640 x 480

# 设定帧数
desired_fps = 30
frame_interval = 1.0 / desired_fps # 帧间隔时间
freq = cv2.getTickFrequency()
frame_rate_calc = 1 # 真实帧率

def generate_frames():
    global frame_rate_calc
    while True:
        t1 = cv2.getTickCount()
        # -----读取等一系列操作开始------
        success, frame = cap.read() # success 是一个bool值
        if not success:
            print("获取图像失败！")
            break
        cv2.putText(frame, 'FPS: {0:.1f}'.format(frame_rate_calc), (480,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        '''
        frame: 画面
        text: 显示文本
        org: 坐标，左上角为(0,0)
        fontFace: 字体，cv2.FONT_HERSHEY_SIMPLEX 是OpenCV提供的一种字体
        fontScale: 字体缩放比例
        color: rgb颜色格式，以BGR的顺序表示
        thickness: 文本线条粗细
        lineType(可选): 抗锯齿
        '''
        ret, buffer = cv2.imencode('.jpg', frame) # 将jpg转换为jpeg格式， ret表示是否转换成功，buffer为转换后的图像数据
        frame = buffer.tobytes() # 将图像数据(jpeg)转换为字节流，通过http发送
        # 输出图像数据，允许在同一个http相应中发送多个部分的内容
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # -------操作结束--------------
        t2 = cv2.getTickCount()
        
        time_cost = (t2 - t1) / freq
        frame_rate_calc = 1 / time_cost 
        
        wait_time = max (0, int(frame_interval - time_cost) * 1000) # 以毫秒计
        time.sleep(wait_time / 1000.0) # time.sleep 需要以秒为单位
            
@app.route('/')
def index():
    # 定义主页，这里的读取方法需要按照文件路径规范
    return render_template('index.html')

@app.route('/video')
def video():
    # 视频流路由
    return Response(generate_frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)