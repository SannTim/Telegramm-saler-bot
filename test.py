from tgsaler import bd_console
from unittest.mock import MagicMock
import unittest

class Test_console(unittest.TestCase):
    def setUp(self) -> None:
        self.app = bd_console.app()
        self.app.bd = MagicMock()
        self.app.bd.add_category =  lambda x: setattr(self, "res", 'Adding category: ' + x)
        self.app.bd.add_product =  lambda x: setattr(self, "res", 'Adding product: ' + x)
        self.app.bd.edit_product =  lambda x: setattr(self, "res", 'Editing product: ' + x)
        return super().setUp()

    def test_add_category(self):
        self.app.onecmd("addcategory name abc")
        print(self.res)

    def test_add_product(self):
        self.app.onecmd("addproduct name abc price 42 category abc")
        print(self.res)

    def test_edit_product(self):
        self.app.onecmd("editproduct name abc")
        print(self.res)