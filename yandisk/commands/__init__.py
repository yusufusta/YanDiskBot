def __list_all_commands():
    from os.path import dirname, basename, isfile
    import glob

    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_commands = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]
    return all_commands

ALL_COMMANDS = sorted(__list_all_commands())
__all__ = ALL_COMMANDS + ["ALL_COMMANDS"]
