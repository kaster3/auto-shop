import inspect


def item_naming() -> str:
    return inspect.stack()[1].function.split("_")[1]
