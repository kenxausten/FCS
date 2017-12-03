# coding:utf8
'''
Created on 2017年11月18日

@author: ilinkin
'''

from cmd import Cmd
from task import FaceTask
import sys
from __builtin__ import str


def parse(line):
    return tuple(line.split(' '))

exec_task = FaceTask()

class BaseShell(Cmd):
    def do_exit(self, args):
        '''exit this program'''
        sys.exit()
    
    def do_quit(self, args):
        '''quit this program'''
        return True
    
    def do_shell(self, args):
        '''run a shell cmd'''
        import subprocess
        subshell = subprocess.Popen(args, shell=True, stdin=None, stdout=None)
        subshell.communicate()
        subshell.terminate()


class FaceShell(BaseShell):
    intro = 'Welcome to the face shell.   Type help or ? to list commands.\n'
    prompt = 'face> '

    def do_show(self, original_arg):
        '''
            1. show facesets ---show all facesets
            2. show faceset <faceset_name> ---show image name in one faceset
        '''
        usage = False
        arg = parse(original_arg)
        if len(arg) == 1:
            if arg[0] == 'facesets':
                print(exec_task.get_facesets())
            else:
                usage = True
        elif len(arg) == 2:
            if arg[0] == 'faceset':
                print(exec_task.get_faceset(arg[1]))
            else:
                usage = True

        if usage:
            self.default(original_arg+ '\n' + "show facesets, show faces facesets_name")

    def do_check(self, original_arg):
        """check identity""" 
        arg = parse(original_arg)

        if len(arg) == 1 and arg[0] == 'identity':
            print(exec_task.search_people_from_camera())
        else:
            self.default(original_arg + '\n' + "check identity")

    def do_upload(self, original_arg):
        """ upload identity """
        arg = parse(original_arg)
        if len(arg) == 1 and arg[0] == 'identity':
            if not exec_task.update_faces_from_camera():
                print('Just work in RASPBERRYPI.')
            else:
                print('update success.')
        else:
            self.default(original_arg+ '\n' + "upload identity ")

    def do_del(self, original_arg):
        """ delete faceset xx """
        arg = parse(original_arg)
        if len(arg) == 2 and arg[0] == 'faceset':
            print('faceset', arg[1])
            exec_task.delete_faceset(arg[1])
        else:
            self.default(original_arg+ '\n' + "del faceset xx")

    def do_add(self, original_arg):
        """ add faceset xx """
        arg = parse(original_arg)
        if len(arg) == 2 and arg[0] == 'faceset':
            exec_task.add_faceset((arg[1]))
        else:
            self.default(original_arg+ '\n' + "add faceset xx")

    def do_exit(self, arg):
        """exit face."""
        return self.clear()

    def do_bye(self, arg):
        """exit face."""
        return self.clear()

    def clear(self):
        print('exit face.')
        exec_task.clear()
        return True


if __name__ == '__main__':
    FaceShell().cmdloop()