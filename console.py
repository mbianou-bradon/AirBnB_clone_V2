#!/usr/bin/python3
"""
Console module for the command interpreter.
"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class.
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User"]

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        Exit the program when End-of-File (EOF) is encountered.
        """
        return True

    def emptyline(self):
        """
        Called when an empty line is entered.
        """
        pass

    def do_create(self, arg):
        """
        Create new instance of a class, save it, and print the id.
        """
        if not arg:
            print("** class name missing **")
            return

        class_name = arg.split()[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        new_instance = eval(class_name)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Print string representation of an instance based on class name and id.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id
        objects = models.storage.all()
        if key in objects:
            print(objects[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on class name and id. Save changes into JSON file.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id
        objects = models.storage.all()
        if key in objects:
            objects.pop(key)
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Print all string representations of instances based on class name.
        If no class name is provided, print all instances of all classes.
        """
        objects = models.storage.all()

        if not arg:
            print([str(obj) for obj in objects.values()])
        else:
            class_name = arg.split()[0]
            if class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return

            print([str(obj) for obj in objects.values() if obj.__class__.__name__ == class_name])

    def do_update(self, arg):
        """
        Update an instance based on class name and id by updating an attribute.
        Save the change into the JSON file.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id
        objects = models.storage.all()
        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        attr_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return

        attr_value = args[3].strip('"')
        instance = objects[key]
        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_count(self, arg):
        """
        Retrieve the number of instances of a class.
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return

        count = sum(isinstance(obj, eval(class_name)) for obj in models.storage.all().values())
        print(count)

    def precmd(self, line):
        """
        Preprocess the command line to handle special commands.
        """
        if ".all()" in line:
            class_name = line.split(".")[0]
            if class_name in self.valid_classes:
                return "all " + class_name

        if ".show(" in line:
            class_name = line.split(".")[0]
            if class_name in self.valid_classes:
                instance_id = line.split("(")[1].split(")")[0]
                return "show " + class_name + " " + instance_id

        if ".destroy(" in line:
            class_name = line.split(".")[0]
            if class_name in self.valid_classes:
                instance_id = line.split("(")[1].split(")")[0]
                return "destroy " + class_name + " " + instance_id

        if ".update(" in line:
            class_name = line.split(".")[0]
            if class_name in self.valid_classes:
                args = line.split("(")[1].split(")")[0].split(", ")
                if len(args) == 3:
                    instance_id = args[0]
                    attr_name = args[1]
                    attr_value = args[2]
                    return "update " + class_name + " " + instance_id + " " + attr_name + " " + attr_value
                elif len(args) == 2:
                    instance_id = args[0]
                    dictionary = eval(args[1])
                    update_args = []
                    for key, value in dictionary.items():
                        update_args.append(instance_id)
                        update_args.append(key)
                        update_args.append(str(value))
                    return "update " + class_name + " " + ", ".join(update_args)

        return line

if __name__ == '__main__':
    HBNBCommand().cmdloop()
