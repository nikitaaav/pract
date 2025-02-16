import subprocess

subprocess.run(["ping", "-c", "4", "google.com"])

try:
    output = subprocess.check_output("ls", shell=True, text=True, encoding='cp866')
    print(output)
    files = output.strip().split('\n')
    print(f"Количество элементов: {len(files)}")
except subprocess.CalledProcessError as e:
    print(f"Ошибка выполнения команды: {e}")
