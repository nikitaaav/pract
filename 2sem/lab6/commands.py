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
    directory.create: """╔════════════════════════════════════════════════════════════════════════════╗
║ Directory Creation Command                                              ║
║ Usage: createDir <path>                                                ║
║ <path>: Target directory path                                          ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    directory.delete: """╔════════════════════════════════════════════════════════════════════════════╗
║ Directory Removal Command                                              ║
║ Usage: deleteDir <path>                                                ║
║ <path>: Directory to remove                                            ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    file.create: """╔════════════════════════════════════════════════════════════════════════════╗
║ File Creation Command                                                  ║
║ Usage: createFile <path>                                               ║
║ <path>: Target file path                                               ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    file.delete: """╔════════════════════════════════════════════════════════════════════════════╗
║ File Removal Command                                                   ║
║ Usage: deleteFile <path>                                               ║
║ <path>: File to remove                                                 ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    file.read: """╔════════════════════════════════════════════════════════════════════════════╗
║ File Reading Command                                                   ║
║ Usage: read <path>                                                     ║
║ <path>: File to read                                                   ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    file.write: """╔════════════════════════════════════════════════════════════════════════════╗
║ File Writing Command                                                   ║
║ Usage: write <path> [--new]                                            ║
║ <path>: Target file                                                    ║
║ --new: Optional flag to overwrite file                                 ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    file.copy: """╔════════════════════════════════════════════════════════════════════════════╗
║ File Copy Command                                                      ║
║ Usage: copy <source> <destination>                                     ║
║ <source>: Source file path                                             ║
║ <destination>: Target file path                                        ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    navigate.go_to: """╔════════════════════════════════════════════════════════════════════════════╗
║ Directory Navigation Command                                           ║
║ Usage: goto <path>                                                     ║
║ <path>: Target directory path                                          ║
╚════════════════════════════════════════════════════════════════════════════╝""",
    get_help: """╔════════════════════════════════════════════════════════════════════════════╗
║ Available Commands                                                     ║
║                                                                        ║
║ • createDir  - Create new directory                                    ║
║ • deleteDir  - Remove directory                                        ║
║ • createFile - Create new file                                         ║
║ • deleteFile - Remove file                                             ║
║ • read       - Read file contents                                      ║
║ • write      - Write to file                                           ║
║ • copy       - Copy file                                               ║
║ • goto       - Navigate to directory                                   ║
║ • help       - Show this help message                                  ║
║                                                                        ║
║ For detailed command info, use: <command> --help                       ║
╚════════════════════════════════════════════════════════════════════════════╝""",
}
