# Тут будут определены все основные команды
from typing import Any, Callable, Sequence, Dict
import directory
import file
import navigate


def execute(command: Callable[..., Any], *args, **kwargs) -> int | str | None:
    """
    Исполняет команду command c аргументами args и kwargs
    :param command: команда для вызова
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    """
    if command == get_help or args[0] in ["-h", "--help"]:
        return get_help(command)

    if len(args) > 1:
        return command(*args, **kwargs)

    return command(*args, **kwargs)


def get_help(command: Callable[..., Any]) -> str:
    """
    Возвращает информацию о команде
    :param command: название команды
    :return: информация о команде
    """
    return HELP_DICT[command]


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

HELP_DICT: Dict[Callable[..., Any], str] = {
    directory.create: """--------------------
Создает директорию.
Синтаксис: createDir src
src: относительный путь до новой директории
--------------------""",
    directory.delete: """--------------------
Удаляет директорию.
Синтаксис: deleteDir src
src: относительный путь до директории
--------------------""",
    file.create: """--------------------
Создает файл.
Синтаксис: createFile src
src: относительный путь до файла
--------------------""",
    file.delete: """--------------------
Удаляет файл.
Синтаксис: deleteFile src
src: относительный путь до файла
--------------------""",
    file.read: """--------------------
Читает файл.
Синтаксис: read src
src: относительный путь до файла
--------------------""",
    file.write: """--------------------
Пишет в файл.
Синтаксис: write src [--new]
src: относительный путь до директории
--new: флаг - если есть, то файл перезаписывается, иначе содержимое добавляется в конец
--------------------""",
    file.copy: """--------------------
Копирует файл.
Синтаксис: copy src dst
src: относительный путь до файла
dst: путь, куда скопировать файл
--------------------""",
    navigate.go_to: """--------------------
Переходит по пути.
Синтаксис: goto src
src: относительный путь до директории
--------------------""",
    get_help: """--------------------
Навигация по командам

createDir: создает директорию
deleteDir: удаляет директорию
createFile: создает файл
deleteFile: удаляет файл
read: читает файл
write: добавляет в конец/перезаписывает файл
copy: копирует файл
goto: переходит в другую папку
help: выводит помощь по всем командам

Чтобы увидеть более точное описание, введите <имя_команды> --help или <имя_команды> -h
--------------------""",
}
