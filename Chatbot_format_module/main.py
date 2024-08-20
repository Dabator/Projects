import os
import shutil
from formato import Formato  
from jerarquia import Jerarquia  




def move_to_final_folder(file_path, final_folder):
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)

    origin_folder_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

    if origin_folder_name == 'docs':
        origin_folder_name = os.path.basename(os.path.dirname(file_path))

    file_name = os.path.basename(file_path)
    file_name_with_folder = f"{file_name}_{origin_folder_name}.md"
    
    destination_path = os.path.join(final_folder, file_name_with_folder)

    if os.path.exists(destination_path):
        base, ext = os.path.splitext(file_name_with_folder)
        counter = 1
        new_destination_path = os.path.join(final_folder, f"{base}_{counter}{ext}.md")
        while os.path.exists(new_destination_path):
            counter += 1
            new_destination_path = os.path.join(final_folder, f"{base}_{counter}{ext}.md")
        destination_path = new_destination_path

    shutil.move(file_path, destination_path)

def copy_to_final_folder(file_path, final_folder):
    if not os.path.exists(final_folder):
        os.makedirs(final_folder)
    
    origin_folder_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

    if origin_folder_name == 'docs':
        origin_folder_name = os.path.basename(os.path.dirname(file_path))
        
    file_name = os.path.basename(file_path)
    file_name_with_folder = f"{file_name}_{origin_folder_name}.md"
    
    destination_path = os.path.join(final_folder, file_name_with_folder)

    if os.path.exists(destination_path):
        base, ext = os.path.splitext(file_name)
        counter = 1
        new_destination_path = os.path.join(final_folder, f"{base}_{counter}{ext}_{origin_folder_name}.md")
        while os.path.exists(new_destination_path):
            counter += 1
            new_destination_path = os.path.join(final_folder, f"{base}_{counter}{ext}_{origin_folder_name}.md")
        destination_path = new_destination_path

    shutil.copy(file_path, destination_path)

def process_file(file_path):
    _, file_name = os.path.split(file_path)
    file_name_without_extension, file_extension = os.path.splitext(file_name)
    final_folder = 'archivos_finales'

    if not file_extension.endswith(".md"): 
        return  

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            original_content = file.read()

    unified_content = original_content
    formato = Formato(unified_content)
    content_changed = False

    input_format = formato.detect_format()

    if input_format is None:
        print(f'Formato no soportado para el archivo: {file_name}')
        print('\n')
        return

    if "```" in unified_content:
        unified_content = formato.change_chunk()
        content_changed = True

    if 'html' in input_format or 'latex' in input_format:
        unified_content = formato.convert_to_md()
        content_changed = True

    jerarquia = Jerarquia(unified_content)
    

    if not jerarquia.detect_title(unified_content) or not jerarquia.detect_structure(unified_content):
        unified_content = jerarquia.correct_structure()
        content_changed = True
    

    if content_changed:
        output_file_path = os.path.splitext(file_path)[0] + '_converted'
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(unified_content)
        move_to_final_folder(output_file_path, final_folder)
    else:
        copy_to_final_folder(file_path, final_folder)

directory_path = 'ruta_directorio_archivos' # Reemplaza con la ruta de tu directorio

for root, _, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        process_file(file_path)