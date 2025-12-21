# fix_encoding.py
import os
import codecs

def convert_to_utf8_without_bom(filepath):
    try:
        # Читаем файл как бинарный
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Пробуем декодировать как UTF-8
        try:
            content.decode('utf-8')
        except UnicodeDecodeError:
            # Если не UTF-8, пробуем другие кодировки
            for encoding in ['cp1251', 'cp1252', 'latin-1', 'iso-8859-1']:
                try:
                    content = content.decode(encoding).encode('utf-8')
                    break
                except:
                    continue
        
        # Удаляем BOM если есть
        if content.startswith(codecs.BOM_UTF8):
            content = content[len(codecs.BOM_UTF8):]
        
        # Записываем обратно в UTF-8 без BOM
        with open(filepath, 'wb') as f:
            f.write(content)
            
        print(f"Fixed: {filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        # Игнорируем скрытые папки и служебные папки cookiecutter
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            # Проверяем только текстовые файлы
            if file.endswith(('.py', '.txt', '.md', '.rst', '.ini', '.cfg', 
                            '.yml', '.yaml', '.json', '.toml', '.html', '.js', 
                            '.css', '.sql', '.sh', '.bat')):
                filepath = os.path.join(root, file)
                convert_to_utf8_without_bom(filepath)

if __name__ == "__main__":
    template_dir = r"D:\TestGrom StoreManager\PythonProject\template"
    process_directory(template_dir)
    print("Encoding fix completed!")