# coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''

from cmd import Cmd
from task import FaceTask

exec_task = FaceTask()

class FaceShell(Cmd):
    intro = 'Welcome to the face shell.   Type help or ? to list commands.\n'
    prompt = '(face) '

    def do_show(self, arg):
        """ show facesets, show faces """
        arg = arg.split(' ')
        print(len(arg))
        if len(arg) == 1:
            if arg[0] == 'facesets':
                print(exec_task.get_facesets())
        elif len(arg) == 2:
            if arg[0] == 'faces':
                print(exec_task.get_faces(arg[1]))
        else:
            self.default(arg[0]+'\n'+ "show facesets, show faces name")

    def do_serach(self, arg):
        u'compare'
        self.default(arg[0])

    def close(self):
        pass

    def do_bye(self):
        print('exit face.')
        return True

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    FaceShell().cmdloop()