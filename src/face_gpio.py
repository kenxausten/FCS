#coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''

from task import RASPBERRYPI, GPIO, FaceTask
from threading import Thread
import time

BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO = 17


class GPIOThread(Thread):
    def __init__(self, *args, **kwargs):
        super(GPIOThread, self).__init__(*args, **kwargs)
        if RASPBERRYPI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO, GPIO.IN)
        self.exec_task = FaceTask()

    def run(self):
        if RASPBERRYPI:
            status = GPIO.input(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO)
            if not status:  # 低电平按键别按下
                time.sleep(0.02)  # 延时20ms, 按键消抖动
                if not GPIO.input(BCM_PIN17_TRIGGER_SHOW_TAKE_PHOTO):  #确认按键按下
                    self.exec_task.search_people_from_camera() # 触发拍照check identity
                else:
                    time.sleep(0.1) # 是抖动，休眠
            else:
                time.sleep(0.1)  # 休眠
        else:
            time.sleep(1)
        print('sleep')


if __name__ == '__main__':
    t = GPIOThread()
    t.start()
    t.sleep(10)