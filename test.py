from tgsaler import bd_console
from unittest.mock import MagicMock
import unittest
import io
import sys

class Test_console(unittest.TestCase):
    def setUp(self) -> None:
        self.app = bd_console.app()
        self.app.bd = MagicMock()
        self.app.bd.add_category =  lambda x: setattr(self, "res", 'Adding category: ' + x)
        self.app.bd.add_product =  lambda *x: setattr(self, "res", 'Adding product:'+ ''.join([*x]))
        self.prod = {'name': 'abc', 'price': 42, 'category':1}
        self.app.bd.get_product_data = lambda x: self.prod
        self.app.bd.edit_produt_by_data =  lambda x: setattr(self, "res",  x)
        return super().setUp()

    def test_add_category(self):
        self.app.onecmd("addcategory name abc")
        self.assertEqual(self.res, 'Adding category: abc')

    def test_add_product(self):
        self.app.onecmd("addproduct name abc price 42 category cats")
        self.assertEqual(self.res, 'Adding product:abccats42руб')

    def test_edit_product(self):
        self.app.onecmd("editproduct name abc price 1337")
        self.assertEqual(self.res, {'name': 'abc', 'price': '1337', 'category':1})

    def test_wrong_data(self):
        output = io.StringIO()
        sys.stdout = output
        self.app.onecmd("addcategory abc")
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue().strip().split(), ['Добавляет', 'новую', 'категорию', 'Использование:', 'addcategory', 'name', '<name>'])