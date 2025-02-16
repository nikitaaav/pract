import os

directory = input("Введите путь для создания директории: ")
if os.path.exists(directory):
    print("Директория уже существует")
else:
    os.makedirs(directory)
    print(f"Директория {directory} создана")

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

directory = input("Введите путь к директории для перечисления файлов: ")
list_files(directory)
