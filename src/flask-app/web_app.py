from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read() # success 是一个bool值
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame) # 将jpg转换为jpeg格式， ret表示是否转换成功，buffer为转换后的图像数据
            frame = buffer.tobytes() # 将图像数据(jpeg)转换为字节流，通过http发送
            # 输出图像数据，允许在同一个http相应中发送多个部分的内容
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/')
def index():
    # 定义主页
    return render_template_string(open('./src/flask-app/templates/index.html').read())# 启用html模板

@app.route('/video')
def video():
    # 视频流路由
    return Response(generate_frames(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)