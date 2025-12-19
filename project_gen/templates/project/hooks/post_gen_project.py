import os
import shutil
from pathlib import Path


def move_directory_contents(src: Path, dst: Path):
    """
    Безопасное перемещение содержимого между директориями на Windows.
    Работает даже при разных дисках.
    """
    # Создаем временную директорию на том же диске, что и исходная
    temp_parent = src.parent

    # Для избежания конфликтов создаем уникальное имя временной директории
    import uuid
    temp_dir = temp_parent / f"temp_move_{uuid.uuid4().hex[:8]}"
    temp_dir.mkdir(exist_ok=True)

    try:
        # 1. Копируем все элементы во временную директорию (на том же диске)
        for item in os.listdir(src):
            src_item = src / item
            temp_item = temp_dir / item

            if os.path.isdir(src_item):
                shutil.copytree(src_item, temp_item, dirs_exist_ok=True)
            else:
                shutil.copy2(src_item, temp_item)

        # 2. Удаляем исходную директорию
        shutil.rmtree(src)

        # 3. Перемещаем из временной в целевую
        for item in os.listdir(temp_dir):
            temp_item = temp_dir / item
            dst_item = dst / item

            # Если цель уже существует, удаляем
            if dst_item.exists():
                if dst_item.is_dir():
                    shutil.rmtree(dst_item)
                else:
                    os.remove(dst_item)

            shutil.move(str(temp_item), str(dst_item))

        # 4. Удаляем временную директорию
        shutil.rmtree(temp_dir)

    except Exception as e:
        # В случае ошибки пытаемся очистить временную директорию
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        raise


def safe_move_current_directory():
    """
    Безопасное перемещение при use_current_directory == 'y'
    """
    current_dir = Path.cwd()
    parent_dir = current_dir.parent

    # Проверяем, что мы в поддиректории (как и ожидается)
    if current_dir.name == "{{ cookiecutter.project_slug }}":
        print(f"Moving contents from {current_dir} to {parent_dir}")

        # Создаем список файлов для перемещения
        items_to_move = list(current_dir.iterdir())

        for item in items_to_move:
            target_path = parent_dir / item.name

            # Если файл уже существует в родительской директории
            if target_path.exists():
                if target_path.is_dir():
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)

            # Перемещаем
            shutil.move(str(item), str(parent_dir))

        # Удаляем пустую директорию проекта
        shutil.rmtree(current_dir)

        print("Successfully moved project to current directory")
    else:
        print(f"Warning: Current directory name '{current_dir.name}' doesn't match project slug '{{ cookiecutter.project_slug }}'")
        print("Skipping directory move...")


if __name__ == "__main__":
    if "{{ cookiecutter.use_current_directory }}".lower().strip() == "y":
        safe_move_current_directory()