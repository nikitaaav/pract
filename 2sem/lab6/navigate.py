# Тут будет реализована навигация по файловой системе внутри рабочей директории.
import os
import root

def go_to(dst: str) -> None:
    """
    Переходит в определенную папку
    :param dst: абсолютный путь до папки, обязательный параметр
    """
    dst = os.path.abspath(dst)

    if not os.path.exists(dst):
        raise FileNotFoundError(f"папка {dst} не найдена.")

    if not os.path.isdir(dst):
        raise NotADirectoryError(f"{dst} не является директорией.")

    root.check_rights(dst)

    os.chdir(dst)
