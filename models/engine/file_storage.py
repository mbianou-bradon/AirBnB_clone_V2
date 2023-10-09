import json
import os
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """Handles serialization and deserialization of instances"""

    __file_path = "file.json"
    __classes = [BaseModel, User]
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        serialized_objects = {}
        for key, value in self.__objects.items():
            serialized_objects[key] = self._serialize_instance(value)

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                serialized_objects = json.load(file)
                for key, value in serialized_objects.items():
                    self.__objects[key] = self._deserialize_instance(value)

    def _serialize_instance(self, instance):
        """Serialize an instance to a dictionary"""
        serialized_instance = instance.to_dict()
        serialized_instance['__class__'] = type(instance).__name__
        return serialized_instance

    def _deserialize_instance(self, serialized_instance):
        """Deserialize a dictionary to an instance"""
        class_name = serialized_instance.pop('__class__', None)
        for cls in self.__classes:
            if class_name == cls.__name__:
                return cls(**serialized_instance)
        return BaseModel(**serialized_instance)
