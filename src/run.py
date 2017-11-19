# coding:utf8

import threading
from face_cmd import FaceShell
from face_gpio import GPIOThread


if __name__ == '__main__':

    # shell_thread = threading.Thread(target=FaceShell().cmdloop())
    # gpio_thread = GPIOThread()
    # shell_thread.start()
    # gpio_thread.start()
    # shell_thread.join()
    # gpio_thread.join()
    FaceShell.cmdloop()


