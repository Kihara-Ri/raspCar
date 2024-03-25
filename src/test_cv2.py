import cv2

# 打印OpenCV版本
print(cv2.__version__)

# 创建一个黑色的图像
image = cv2.imread("./assets/lena.jpeg")

# 将图像转换为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 保存灰度图
cv2.imwrite("./assets/gray_image.jpg", gray_image)
