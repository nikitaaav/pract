from typing import List, Callable, Any
import commands

running = True

print("""
Привет! Приветствую Вас в файловом менеджере!
С ним вы сможете создавать и удалять директории, а также создавать, перемещать, копировать и удалять файлы, а также много чего другого!
Напишите "help", чтобы получить подробности по командам.

Также вы можете написать --help/-h после каждой команды, чтобы получить информацию по ним (например, createDir --help).
""")

while running:
    raw = input("Input a command: ")

def determine_command(command: str) -> List[Callable[..., Any], List[Any]]:
    pass

def get_abs_path():
    pass
