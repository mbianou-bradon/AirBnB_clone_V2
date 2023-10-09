import unittest
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """
    Unit tests for the FileStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class.
        """
        cls.file_path = "test_file.json"
        cls.storage = FileStorage()
        cls.storage._FileStorage__file_path = cls.file_path

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after the test class.
        """
        if os.path.exists(cls.file_path):
            os.remove(cls.file_path)

    def tearDown(self):
        """
        Clean up after each test.
        """
        self.storage._FileStorage__objects = {}

    def test_all(self):
        """
        Test the all() method.
        """
        # Create two BaseModel instances
        obj1 = BaseModel()
        obj2 = BaseModel()

        # Add the instances to the storage
        self.storage.new(obj1)
        self.storage.new(obj2)

        # Get all objects from the storage
        all_objects = self.storage.all()

        # Check if the objects are present in the dictionary
        self.assertIn("BaseModel.{}".format(obj1.id), all_objects)
        self.assertIn("BaseModel.{}".format(obj2.id), all_objects)

    def test_new(self):
        """
        Test the new() method.
        """
        # Create a new BaseModel instance
        obj = BaseModel()

        # Add the instance to the storage
        self.storage.new(obj)

        # Check if the object is present in the dictionary
        self.assertIn("BaseModel.{}".format(obj.id), self.storage.all())

    def test_save_reload(self):
        """
        Test the save() and reload() methods.
        """
        # Create a new BaseModel instance
        obj = BaseModel()

        # Add the instance to the storage
        self.storage.new(obj)

        # Save the objects to the file
        self.storage.save()

        # Check if the file exists
        self.assertTrue(os.path.exists(self.file_path))

        # Clear the objects from the storage
        self.storage._FileStorage__objects = {}

        # Reload the objects from the file
        self.storage.reload()

        # Get the reloaded objects
        reloaded_objects = self.storage.all()

        # Check if the reloaded objects are equal to the original objects
        self.assertEqual(len(reloaded_objects), 1)
        self.assertIn("BaseModel.{}".format(obj.id), reloaded_objects)

        # Check if the reloaded object has same attributes as original object
        reloaded_obj = reloaded_objects["BaseModel.{}".format(obj.id)]
        self.assertEqual(reloaded_obj.id, obj.id)
        self.assertEqual(reloaded_obj.created_at, obj.created_at)
        self.assertEqual(reloaded_obj.updated_at, obj.updated_at)

    def test_reload_no_file(self):
        """
        Test the reload() method when the file does not exist.
        """
        # Remove the file if it exists
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

        # Reload the objects from the file (should not raise an exception)
        self.storage.reload()

        # Check if the objects are empty
        self.assertEqual(len(self.storage.all()), 0)


if __name__ == '__main__':
    unittest.main()
