# Тут будут определены все основные команды
from typing import Any, Callable, Sequence, Dict
import directory
import file
import navigate


def execute(command: Callable[..., Any], args: Sequence[Any], kwargs: Dict[str, Any]) -> int | None:
    """
    Исполняет команду command c аргументами args и kwargs
    :param command: команда для вызова
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    """
    return command(*args, **kwargs)

def get_help(command: str) -> str:
    """
    Возвращает информацию о команде
    :param command: название команды
    :return: информация о команде
    """
    return command.__doc__

COMMAND_DICT: Dict[str, Callable[..., Any]] = {
    "createDir": directory.create,
    "deleteDir": directory.delete,
    "createFile": file.create,
    "deleteFile": file.delete,
    "read": file.read,
    "write": file.write,
    "copy": file.copy,
    "goto": navigate.go_to,
    "help": get_help,
}

