# Тут будет реализовано создание и удаление директорий.
import os
import shutil
import root


def create(src: str) -> None:
    """
    Создает новую папку
    :param src: абсолютный путь до новой папки, обязательный параметр
    """
    if os.path.exists(src):
        raise FileExistsError(f"папка {src} уже существует.")

    root.check_rights(src)

    os.makedirs(src, exist_ok=True)


def delete(src: str) -> int:
    """
    Удаляет папку
    :param src: абсолютный путь до папки, обязательный параметр
    :return: размер папки, которая была удалена
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"папка {src} не найдена.")

    root.check_rights(src)

    size = sum(sum(os.path.getsize(os.path.join(root, file)) for file in files) for root, _, files in os.walk(src))
    shutil.rmtree(src)

    return size


