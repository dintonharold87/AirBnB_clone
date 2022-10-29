#!/usr/bin/python3
""" creates a command line interpreter"""


import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """Creates a console class"""
    prompt = '(hbnb) '
    lastcmd = 'exit'
        
    def emptyline(self):
        return

    def do_quit(self, arg):
        'Quit command to exit the program\n'
        sys.exit(1)

    def do_EOF(self, arg):
        'Quit command to exit the program\n'
        sys.exit(1)

#Cmd.emptyline()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
