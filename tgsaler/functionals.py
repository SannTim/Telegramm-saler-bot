"""Дополнительные функции."""
import configparser


def ini_to_dict(file_path):
    """Считывает файл .ini и переводит его в словарь."""
    config = configparser.ConfigParser()
    config.read(file_path)

    ini_dict = {}
    for section in config.sections():
        section_dict = {}
        for key, value in config.items(section):
            section_dict[key] = value
        ini_dict[section] = section_dict

    return ini_dict
