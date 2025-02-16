from typing import List, Callable, Dict
import commands
import os

ROOT_DIR = os.getcwd()


def determine_command(str_cmd: str) -> [Callable[..., any], List[str], Dict[str, bool]]:
    """
    Соотносит строковое представление команды с функцией
    :param str_cmd: строковое представление команды
    :return: возвращает функцию и аргументы к ней
    """

    def get_commands(cmds: List[str]) -> List[str]:
        """
        Возвращает аргументы из команды (позиционные)
        :param cmds: список всех аргументов
        :return: массив позиционных аргументов
        """
        args = []
        for cmd in cmds:
            if not cmd.startswith("--"):
                args.append(cmd)
        return args

    def get_flags(cmds: List[str]) -> Dict[str, bool]:
        """
        Возвращает флаги из команд (например, --new -> {"new": True})
        :param cmds: список всех аргументов
        :return: словарь флагов
        """
        flags = {}
        for cmd in cmds:
            if cmd.startswith("--"):
                flags[cmd[2:]] = True
        return flags

    split_command = str_cmd.strip().split(" ")
    if commands.COMMAND_DICT.get(split_command[0]):
        cmd = commands.COMMAND_DICT.get(split_command[0])
        args = get_commands(split_command[1:])
        flags = get_flags(split_command[1:])
        return cmd, args, flags
    raise Exception("ввод инвалидной команды")


print("""
Приветствую Вас в файловом менеджере!
С ним вы сможете создавать и удалять директории, а также создавать, перемещать, копировать и удалять файлы, а также много чего другого!
Напишите "help", чтобы получить подробности по командам.

      _,---.       _,.---._                                 .=-.-.  .-._
  _.='.'-,  \    ,-.' , -  `.       _..---.      _.-.      /==/_ / /==/ \  .-._
 /==.'-     /   /==/_,  ,  - \    .' .'.-. \   .-,.'|     |==|, |  |==|, \/ /, /
/==/ -   .-'   |==|   .=.     |  /==/- '=' /  |==|, |     |==|  |  |==|-  \|  |
|==|_   /_,-.  |==|_ : ;=:  - |  |==|-,   '   |==|- |     |==|- |  |==| ,  | -|
|==|  , \_.' ) |==| , '='     |  |==|  .=. \  |==|, |     |==| ,|  |==| -   _ |
\==\-  ,    (   \==\ -    ,_ /   /==/- '=' ,| |==|- `-._  |==|- |  |==|  /\ , |
 /==/ _  ,  /    '.='. -   .'   |==|   -   /  /==/ - , ,/ /==/. /  /==/, | |- |
 `--`------'       `--`--''     `-._`.___,'   `--`-----'  `--`-`   `--`./  `--`


Также вы можете написать --help/-h после каждой команды, чтобы получить информацию по ним (например, createDir --help).

Если захотите выйти, напишите exit.
""")


def run():
    while True:
        raw = input("$ ")
        if raw.strip() == "exit":
            break
        try:
            command, args, kwargs = determine_command(raw)
            output = commands.execute(command, *args, **kwargs)
            if output:
                print(f"{output} байт было изменено.")
        except Exception as err:
            print("Возникла ошибка:", err)
