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

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def emptyline(self):
        return

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def do_EOF(self, line):
        """Handles End Of File character.
        """
        print()
        return True

    def do_create(self, line):
        """Creates an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

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
                    li = re.search(arg, k)
                    if li is not None:
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

    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
