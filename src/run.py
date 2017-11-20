# coding:utf8

import threading
from face_cmd import FaceShell
from face_gpio import GPIO_spin, Signal


if __name__ == '__main__':
    signal = Signal()
    shell_thread = threading.Thread(target=FaceShell().cmdloop())
    gpio_thread = threading.Thread(target=GPIO_spin, args=(signal,))
    shell_thread.start()
    gpio_thread.start()
    shell_thread.join()
    signal.go = False
    gpio_thread.join()


