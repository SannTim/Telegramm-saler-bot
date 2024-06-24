"""Модуль, реализующий консоль."""

from tgsaler import bd_worker
import cmd
import shlex
import gettext
import os

curloc = "ru"


def _(*args):
    return LOCALES[curloc].gettext(*args)


trans_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../translations"))

LOCALES = {
    "ru": gettext.translation("tgsaler", trans_dir, ["ru"]),
    "en": gettext.NullTranslations(),
}


class app(cmd.Cmd):
    """Класс, реализующий интерфейс командной строки."""

    prompt = "> "

    def preloop(self) -> None:
        """Настройка перед запуском интерактивной сессии."""
        self.bd = bd_worker.db_controller()
        return super().preloop()

    def do_addcategory(self, args):
        """
        Добавляет новую категорию продуктов.

        :param str args: Аргументы команды
        """
        lexer = shlex.shlex(args, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = " "
        lexer.quotes = ['"', "'"]
        tokens = list(lexer)
        try:
            name = tokens[tokens.index("name") + 1]
            if tokens.index("name") == -1:
                raise Exception
            self.bd.add_category(name)
        except Exception:
            self.help_addcategory()

    def do_addproduct(self, args):
        """
        Добавляет новый продукт.

        :param str args: Аргументы команды
        """
        lexer = shlex.shlex(args, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = " "
        lexer.quotes = ['"', "'"]
        tokens = list(lexer)
        try:
            currency = _("$")
            descr = ""
            photo = ""
            if args.find("currency") != -1:
                currency = tokens[tokens.index("currency") + 1]

            if args.find("descr") != -1:
                descr = tokens[tokens.index("descr") + 1]

            if args.find("photo") != -1:
                photo = tokens[tokens.index("photo") + 1]

            name = tokens[tokens.index("name") + 1]
            category = tokens[tokens.index("category") + 1]
            price = tokens[tokens.index("price") + 1]
            self.bd.add_product(name, category, price, currency, descr, photo)
        except Exception:
            self.help_addproduct()

    def do_delproduct(self, args):
        """
        Удаляет продукт.

        :param str args: Аргументы команды
        """
        lexer = shlex.shlex(args, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = " "
        lexer.quotes = ['"', "'"]
        tokens = list(lexer)
        try:
            name = tokens[tokens.index("name") + 1]
            if tokens.index("name") == -1:
                raise Exception
            self.bd.del_product(name)
        except Exception:
            self.help_delproduct()

    def do_delcategory(self, args):
        """
        Удаляет категорию продуктов.

        :param str args: Аргументы команды
        """
        lexer = shlex.shlex(args, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = " "
        lexer.quotes = ['"', "'"]
        tokens = list(lexer)
        try:
            name = tokens[tokens.index("name") + 1]
            if tokens.index("name") == -1:
                raise Exception
            self.bd.del_category(name)
        except Exception:
            self.help_delcategory()

    def do_editproduct(self, args):
        """
        Редактирует данные о продукте.

        :param str args: Аргументы команды
        """
        lexer = shlex.shlex(args, posix=True)
        lexer.whitespace_split = True
        lexer.whitespace = " "
        lexer.quotes = ['"', "'"]
        tokens = list(lexer)

        try:
            name = tokens[tokens.index("name") + 1]
            if tokens.index("name") == -1:
                raise Exception
            pr = self.bd.get_product_data(name)
            if args.find("currency") != -1:
                currency = tokens[tokens.index("currency") + 1]
                pr["currency"] = currency
            if args.find("descr") != -1:
                descr = tokens[tokens.index("descr") + 1]
                pr["descr"] = descr
            if args.find("photo") != -1:
                photo = tokens[tokens.index("photo") + 1]
                pr["photo"] = photo
            if args.find("price") != -1:
                price = tokens[tokens.index("price") + 1]
                pr["price"] = price
            if args.find("category") != -1:
                category = tokens[tokens.index("category") + 1]
                pr["category"] = category
            self.bd.edit_produt_by_data(pr)
        except Exception:
            self.help_editproduct()

    def do_lang(self, args):
        """
        Изменяет язык интерфейса.

        :param str args: Аргументы команды
        """
        # print(args.split()[-1])
        global curloc
        if len(args) > 0 and args.split()[-1] in LOCALES.keys():
            curloc = args.split()[-1]
            print(_("Language changed to"), args.split()[-1])
        else:
            self.help_lang()

    def help_lang(self):
        """Выводит справку по команде lang."""
        print(_("Changes language to chosen one"))

    def do_showproducts(self, args):
        """
        Отображает таблицу всех продуктов.

        :param str args: Аргументы команды
        """
        print(self.bd.show_product())

    def do_showcategory(self, args):
        """
        Отображает таблицу всех категорий.

        :param str args: Аргументы команды
        """
        print(self.bd.show_category())

    def help_showproducts(self):
        """Выводит справку по команде showproducts."""
        print(_("Shows products table"))
        print(_("Usage: showproducts"))

    def help_showcategory(self):
        """Выводит справку по команде showcategory."""
        print(_("Shows category table"))
        print(_("Usage: showcategory"))

    def help_addcategory(self):
        """Выводит справку по команде addcategory."""
        print(_("Adds new category"))
        print(_("Usage: addcategory name <name>"))

    def help_addproduct(self):
        """Выводит справку по команде addproduct."""
        print(_("Adds new product"))
        print(
            _(
                "Usage: addproduct name <name> price <price> descr <descr> currency <currency> photo <photo> category <category>"
            )
        )

    def help_delproduct(self):
        """Выводит справку по команде delproduct."""
        print(_("Deletes product"))
        print(_("Usage: delproduct name <name>"))

    def help_editproduct(self):
        """Выводит справку по команде editproduct."""
        print(_("Edits new product"))
        print(
            _(
                "Usage: editproduct name <name> price <price> descr <descr> currency <currency> photo <photo> category <category>"
            )
        )

    def help_delcategory(self):
        """Выводит справку по команде delcategory."""
        print(_("Deletes category"))
        print(_("Usage: delcategory name <name>"))

    def do_EOF(self, args):
        """
        Обработчик команды EOF (Ctrl+D).

        :param str args: Аргументы команды
        :return: Флаг завершения сессии
        :rtype: bool
        """
        return True
