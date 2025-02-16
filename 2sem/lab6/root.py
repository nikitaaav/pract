import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_rights(src: str) -> None:
    """
    Проверяет права на определенную папку/файл (мы не можем взаимодействовать с файлами вне родной директории)
    :param src: путь до файла/папки
    """
    src = os.path.abspath(src)
    if not src.startswith(ROOT_DIR):
        raise PermissionError(f"у вас нет прав на {src}")
