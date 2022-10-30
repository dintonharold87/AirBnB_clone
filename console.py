#!/usr/bin/python3
""" creates a command line interpreter"""

from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import cmd
import sys
import json
import re

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
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
        if len(words) < 2 or words[1] == "":
            print("** instance id missing **")
        else:
            if "{}.{}".format(words[0], words[1]) in storage.all():
                    print(storage.all()["{}.{}".format(words[0], words[1])])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """destroy a basemodel"""
        if line == "":
            print("** class name missing **")

        words = line.split(" ")
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
        if len(words) < 2 or words[1] == "":
            print("** instance id missing **")
        else:
            key = "{}.{}".format(words[0], words[1])
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        'prints all string representation of all instaces'
        if arg != "" and arg not in storage.classes():
            print("** class doesn't exist **")
        else:
            y = []
            if arg == '':
                for k, v in storage.all().items():
                    y.append(str(v))
            else:
                for k, v in storage.all().items():
                    l = re.search(arg, k)
                    if l != None:
                        y.append(str(v))
            print(y)

    def do_update(self, line):
        'updates an instance based on the classname and id'
        if line == "":
            print("** class name missing **")
            return
        words = line.split(" ")
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(words) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(words[0], words[1]) 
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(words) == 2:
            print("** attribute name missing **")
            return
        if len(words) == 3:
            print("** value missing **")
            return
        storage.reload()
        setattr(storage.all()[key], words[2], words[3])
        storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
