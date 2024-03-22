import curses
from ROBOT_CONTROL import ROBOT
import time
import Adafruit_PCA9685

# 初始化机器人底层控制
robot = ROBOT()
pwm = Adafruit_PCA9685.PCA9685(busnum = 1)
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))

# 频率设置为50hz，适用于舵机系统。
pwm.set_pwm_freq(50)
angle_b = 90
angle_t = 90
set_servo_angle(9,90)  # 底部舵机 90
set_servo_angle(10,90)  # 顶座舵机 90 

def control_car(stdscr, key, current_line, max_y):
    global angle_b
    global angle_t
    message = ""
    if key == ord('w'):
        robot.t_up()  # Using default speed
        message = "Moving forward...\n"
    elif key == ord('s'):
        robot.t_down()  # Assuming t_down similar to t_up
        message = "Moving backward...\n"
    elif key == ord('a'):
        robot.turnLeft()  # Assuming turnLeft similar to t_up
        message = "Turning left...\n"
    elif key == ord('d'):
        robot.turnRight()  # Assuming turnRight similar to t_up
        message = "Turning right...\n"
    elif key == ord('e'):
        robot.t_stop(0)
        message = "Stopping...\n"
        
        # 舵机
    elif key == ord('h'):
        angle_b = angle_b - 5
        set_servo_angle(9, angle_b)
        message = f"current angle of bottom: {angle_b} "
    elif key == ord('l'):
        angle_b = angle_b + 5
        set_servo_angle(9, angle_b)
        message = f"current angle of bottom: {angle_b} "
    elif key == ord('j'):
        angle_t = angle_t - 5
        set_servo_angle(10, angle_t)
        message = f"current angle of top: {angle_t} "
    elif key == ord('k'):
        angle_t = angle_t + 5
        set_servo_angle(10, angle_t)
        message = f"current angle of top: {angle_t} "

    if message:
        if current_line >= max_y - 2:
            stdscr.clear()
            stdscr.addstr("Control the robot with W A S D keys, press E to stop, and press Q to exit.\n")
            current_line = 1
        else:
            current_line += 1
        stdscr.addstr(current_line, 0, message)
        stdscr.refresh()
    return current_line

def main(stdscr):
    # 设置curses环境
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    current_line = 0
    stdscr.addstr(current_line, 0, "Control the robot with W A S D keys, press E to stop, and press Q to exit.\n")
    current_line += 1

    while True:
        key = stdscr.getch()
        current_line = control_car(stdscr, key, current_line, max_y)
        if key == ord('q'):
            robot.t_stop()
            break

    # 恢复终端状态
    stdscr.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

curses.wrapper(main)

