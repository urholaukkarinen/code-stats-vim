"""Mock implementation of the `vim` module."""

_eval = {}
_commands = []


def eval(var):
    # raise if not found
    return _eval[var]


def command(cmd):
    _commands.append(cmd)


def set_eval(vars):
    global _eval
    _eval = vars


def get_commands():
    return _commands


def clear_commands():
    global _commands
    _commands = []
