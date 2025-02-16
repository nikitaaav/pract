# Тут будут расположены основные команды взаимодействия с файлами - создание, чтение, запись, удаление, копирование,
# перемещение и переименование файлов.
import os
import shutil
import root


def create(src: str, content: str = "") -> int:
    """
    Создает новый файл
    :param src: абсолютный путь до файла, обязательный параметр
    :param content: содержание файла, по умолчанию равно ""
    """
    if os.path.exists(src):
        raise FileExistsError(f"файл {src} уже существует.")

    root.check_rights(src)

    with open(src, "w", encoding="utf-8") as f:
        f.write(content)

    return os.path.getsize(src)


def delete(src: str) -> int:
    """
    Удаляет файл
    :param src: абсолютный путь до файла, обязательный параметр
    :return: размер удаленного файла
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"файл {src} не найден.")

    root.check_rights(src)

    size = os.path.getsize(src)
    os.remove(src)
    return size


def read(src: str) -> str:
    """
    Читает файл и возвращает его содержимое
    :param src: абсолютный путь до файла, обязательный параметр
    :return: содержание файла
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"файл {src} не найден.")

    root.check_rights(src)

    with open(src, "r", encoding="utf-8") as f:
        return f.read()


def write(src: str, content: str, new: bool = False) -> int:
    """
    Дописывает в конец файла информацию (либо перезаписывает его полностью)
    :param src: абсолютный путь до файла, обязательный параметр
    :param content: данные для записи
    :param new: флаг, указывающий, перезаписывать ли файл (new==True) или нет (new==False)
    :return: размер нового файла
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"файл {src} не найден.")

    root.check_rights(src)

    old_size = os.path.getsize(src)

    with open(src, "w" if new else "a", encoding="utf-8") as f:
        f.write(content + "\n")

    return os.path.getsize(src) - old_size


def copy(src: str, dst: str) -> int:
    """
    Копирует файл из src в dst
    :param src: абсолютный путь до файла
    :param dst: абсолютный путь, куда необходимо копировать файл
    :return: размер файла, который был скопирован
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"файл {src} не найден.")

    if os.path.exists(dst):
        raise FileExistsError(f"файл {src} уже существует.")

    root.check_rights(src)

    root.check_rights(dst)

    shutil.copy(src, dst)
    return os.path.getsize(src)
