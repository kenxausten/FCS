#coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''

from task import RASPBERRYPI, GPIO, FaceTask
import threading
import time

BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO = 17


class Signal:
    go = True


def GPIO_spin(signal):
    if RASPBERRYPI:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO, GPIO.IN)
        exec_task = FaceTask()
        while True:
            status = GPIO.input(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO)
            if status:  # 高电平触发check identity
                time.sleep(0.02)  # 延时20ms, 按键消抖动
                if GPIO.input(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO):  #确认高电平触发
                    print('GPIO Trigger check indentity.')
                    print(exec_task.search_people_from_camera()) # 触发拍照check identity
                else:
                    time.sleep(0.1) # 是抖动，休眠
            else:
                time.sleep(0.1)  # 休眠
            if not signal.go:
                break
    else:
        time.sleep(1)


if __name__ == '__main__':
    signal = Signal()
    t = threading.Thread(target=GPIO_spin, args=(signal,))
    t.start()
    t.join