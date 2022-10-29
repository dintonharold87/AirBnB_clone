#!/usr/bin/python3
""" creates a command line interpreter"""

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import cmd
import sys
import json


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

    def do_create(self, arg):
        'Creates a new instance of BaseModdel'
        if arg == "":
            print("** class name missing **")
        elif arg != 'BaseModel':
            print("** class doesn't exist **")
        else:
            dummy = BaseModel()
            dummy.save()
            dict_dummy = dummy.to_dict()
            print(dict_dummy['id'])

    def do_show(self, line):
        "Prints the string rep of an instance"
        if line == "":
            print("** class name missing **")
            return

        words = line.split(" ")
        if words[0] != "BaseModel":
            print("** class doesn't exist **")
        if len(words) < 2 or words[1] == "":
            print("** instance id missing **")
        else:
            with open("file.json", 'r') as f:
                j = json.load(f)
            try:
                if j["BaseModel.{}".format(words[1])]['id']:
                    print(storage.all()["BaseModel.{}".format(words[1])])
            except KeyError:
                print("** no instance found **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
