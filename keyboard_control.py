import curses
from LOBOROBOT import LOBOROBOT
import time

# 初始化小车
robot = LOBOROBOT()

def control_car(stdscr, key, current_line, max_y):
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

# Adjusted t_up function to have a default speed value
def t_up(self, speed=50, t_time=0):
    self.MotorRun(0, 'forward', speed)
    self.MotorRun(1, 'forward', speed)
    self.MotorRun(2, 'forward', speed)
    self.MotorRun(3, 'forward', speed)
    if t_time > 0:
        time.sleep(t_time)

curses.wrapper(main)

