import bd_worker
import cmd
import shlex
import gettext
import locale
import os

curloc="ru"

def _(*args):
    return LOCALES[curloc].gettext(*args)

trans_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "./trans"))

LOCALES = {
    "ru": gettext.translation("mood", trans_dir, ["ru"]),
    "en": gettext.NullTranslations(),
}


class app(cmd.Cmd):
    prompt = "> "

    def preloop(self) -> None:
        self.bd = bd_worker.db_controller()
        return super().preloop()

    def do_addcategory(self, args):
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

    def do_showproducts(self, args):
        print(self.bd.show_product())

    def do_showcategory(self, args):
        print(self.bd.show_category())

    def help_showproducts(self):
        print(_("Shows products table"))
        print(_("Usage: showproducts"))

    def help_showcategory(self):
        print(_("Shows category table"))
        print(_("Usage: showcategory"))

    def help_addcategory(self):
        print(_("Adds new category"))
        print(_("Usage: addcategory name <name>"))

    def help_addproduct(self):
        print(_("Adds new product"))
        print(
            _("Usage: addproduct name <name> price <price> descr <descr> currency <currency> photo <photo> category <category>")
        )

    def help_delproduct(self):
        print(_("Deletes product"))
        print(_("Usage: delproduct name <name>"))

    def help_editproduct(self):
        print(_("Edits new product"))
        print(
            _("Usage: editproduct name <name> price <price> descr <descr> currency <currency> photo <photo> category <category>")
        )

    def help_delcategory(self):
        print(_("Deletes category"))
        print(_("Usage: delcategory name <name>"))

    def do_EOF(self, args):
        return True


cm = app()
cm.cmdloop()
