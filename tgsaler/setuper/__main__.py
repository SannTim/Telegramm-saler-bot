from . import bd_creator, config_creator


def run_main():
    bd_creator.create_db()
    config_creator.create_config()


run_main()
