#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

def parse(arg):
    curly_brackets = re.search(r"\{. * ?}", arg)
    brackets = re.search(r"\[ . * ? ]", arg)
    if curly_brackets is None:
        if brackets is None:
         return[i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_brackets.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_brackets.group())
        return retl

class HBNBCommand(cmd.Cmd):
    prompt = "hbnb"
    __classes = {
        "BaseModel", 
        "User", 
        "State", 
        "City", 
        "Place", 
        "Amenity", 
        "Review"
    }
    
    def empty_line():
        pass
    
    def default(self, arg):
        all_dict = {
            "all" : self.do_all,
            "show" : self.do_show, 
            "destroy" : self.do_destroy,
            "count" : self.do_count,
            "update" : self.do_update
        }
        match = re.search(r"\.", arg)
        if match is None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"((. * ?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0], match.group()[1:-1]]]
                if command[0]in all_dict.keys():
                    call = "{}{}".format(argl[0], command[1])
                    return all_dict[command[0]](call)
        print("****Error syntax : {}".format(arg))
        return False
    def do_quit(self, arg):
        return True
    def do_EOF(self, arg):
        print("")
        return True
    def do_create(self, arg):
        argl = parse(arg)
        if len(argl) == 0:
            print("***Class is missing***")
        elif argl[0] not in HBNBCommand.__classes:
            print("***Class isn't found , try again***")
        else:
            print(eval(argl[0]().id))
            storage.save()
    def do_show(self, arg):
        argl = parse(arg)
        obj_dict = storage.all()
        if len(argl) == 0:
            print("***Class is missing***")
        elif argl[0] not in HBNBCommand.__classes:
            print("***Class isn't found, Try again***")
        elif len(argl) == 1:
            print("***ID is missing***")
        elif "{}.{}".format(argl[0], argl[1]) not in obj_dict:
            print("***No instance is found***")
        else:
            print(obj_dict["{}.{}".format(argl[0], argl[1])])
    def do_destroy(self, arg):
        argl = parse(arg)
        obj_dict = storage.all()
        if len(argl) == 0:
            print("***Class is missing***")
        elif argl[0] not in HBNBCommand.__classes:
            print("***Class isn't found, Try again***")
        elif len(argl) == 1:
            print("***ID is missing***")
        elif "{}.{}".format(argl[0], argl[1])not in obj_dict.keys():
            print("***No instance is found***")
        else:
            del obj_dict["{}.{}".format(argl[0], argl[1])]
            storage.save()
    def do_all(self, arg):
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("***Class isn't found ,try again***")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__)
                elif len(argl) == 0:
                    objl.append(obj.__str__)
            print (objl)
    def do_count(self, arg):
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)
    def do_update(self, arg):
        argl = parse(arg)
        obj_dict = storage.all()
        
        if len(argl) == 0:
            print("***Class ia missing***")
        if argl[0] not in HBNBCommand.__classes:
            print("***Class isn't found, Try again***")
            return False
        if len(argl) == 1 :
            print("***ID is missing***")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in obj_dict.keys():
            print("***Instance is missed***")
            return False
        if len(argl) == 2:
            print("***Attribute is missing")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("***Value is missing")
                return False
            
            if len(argl) == 4 :
                obj = obj_dict["{}.{}".format(argl[0], argl[1])]
                if argl[2]in obj.__class__.__dict__.keys():
                    valtype = type(obj.__class__.__dict__[argl[2]])
                    obj.__dict__[argl[2]] = valtype(argl[3])
                else:
                    obj.__dict__[argl[2]] = argl[3]
            elif type(eval(argl[2])) == dict:
                obj = obj_dict["{}.{}".format(argl[0], argl[1])]
                for x, y in eval(argl[2]).items():
                    if (x in obj.__class__.__dict__.keys() and 
                        type(obj.__class__.__dict__[x] in {str, int, float})):
                        valtype = type(obj.__class__.__dict__[x])
                        obj.__dict__[x] = valtype(y)
                    else:
                        obj.__dict__[x] = y
            storage.save()
    if __name__ == "__main__":
        HBNBCommand().cmdloop()
                
         
