import re
from transformers import pipeline
import urllib3
from nltk.tree import Tree


# Desactivar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Jerarquia:
    def __init__(self, content):
        self.content = content
        self.title = None

    @staticmethod
    def detect_title(content):
        for line in content:
            line = line.strip()
            if line.startswith('#') or line.startswith('<h1>'):
                return True
        return False

    @staticmethod
    def detect_structure(content):
        levels = [False] * 5
        h1_count = 0

        for line in content.split('\n'):
            match = re.match(r'^(#+)\s*(.*)', line)
            if not match:
                continue
            
            level = len(match.group(1))
            if level == 1:
                h1_count += 1
                if h1_count > 1:
                    return False
                levels[0] = True
            elif level <= 5:
                if not all(levels[:level-1]):
                    return False
                levels[level-1] = True
            elif level == 6:
                if not all(levels):
                    return False

        return True

    @staticmethod
    def extract_phrases(tree):
        phrases = []
        for subtree in tree:
            if isinstance(subtree, Tree):
                if subtree.label() in ['NP', 'NE']:
                    phrase = ' '.join([word for word, tag in subtree.leaves()])
                    phrases.append(phrase)
        return phrases

    @staticmethod
    def create_title_from_content(content, max_length=50):
        # Crear el pipeline para generación de texto
        try:
            pipe = pipeline("text2text-generation", model="czearing/article-title-generator")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return "Título no disponible"
        
        # Generar el título
        try:
            result = pipe(content, max_new_tokens=max_length, num_return_sequences=1)
            generated_title = result[0]['generated_text']
            return generated_title.strip()
        except Exception as e:
            print(f"Error al generar el título: {e}")
            return "Título no disponible"
    
    def ensure_title(self, lines):
        if not Jerarquia.detect_title(self.content):
            first_line = lines[0].strip()
            if not first_line.startswith('#'):
                title = Jerarquia.create_title_from_content(self.content)
                lines.insert(0, f'# {title}')
                self.title = title  # Asignar el título creado a la variable de instancia
                print(f'Title created: {title}')
            else:
                lines[0] = re.sub(r'^#+', '#', first_line.strip())

    def normalize_headers(self, lines):
        corrected_lines = []
        last_header_level = 0
        first_h1_found = False

        i = 0
        hashtag_lines_count = 1

        # Contar la cantidad de encabezados en total, tanto markdown como html
        for line in lines:
            if line.startswith('#') or re.match(r'<h[1-6]>', line.strip(), re.IGNORECASE):
                hashtag_lines_count += 1

        compare_level = [0] * hashtag_lines_count
        compare_level[0] = 0

        for line in lines:
            current_header_level = None
            if line.startswith('#'):
                current_header_level = line.count('#')
            else:
                # Detectar encabezados HTML (h1, h2, h3, h4, h5, h6)
                match = re.match(r'<h([1-6])>', line.strip(), re.IGNORECASE)
                if match:
                    current_header_level = int(match.group(1))

            if current_header_level is not None:
                compare_level[i+1] = current_header_level

                # Caso en el que hay más de un título de nivel 1
                if current_header_level == 1:
                    if not first_h1_found:
                        first_h1_found = True
                    else:
                        current_header_level = 2

                # Caso en el que hay dos secciones iguales mal jerarquizadas
                if current_header_level == compare_level[i] and last_header_level > 1:
                    current_header_level = last_header_level

                # Caso en el que hay salto entre secciones
                if current_header_level > last_header_level + 1:
                    current_header_level = last_header_level + 1

                # Actualizar el encabezado dependiendo de su tipo (Markdown o HTML)
                if line.startswith('#'):
                    line = '#' * current_header_level + ' ' + line.lstrip('#').strip()
                else:
                    # Si es un encabezado HTML, ajustar el nivel en la etiqueta
                    line = re.sub(r'<h[1-6]>', f'<h{current_header_level}>', line, flags=re.IGNORECASE)
                    line = re.sub(r'</h[1-6]>', f'</h{current_header_level}>', line, flags=re.IGNORECASE)

                last_header_level = current_header_level
                i += 1

            corrected_lines.append(line)

        return corrected_lines

    def correct_structure(self):
        lines = self.content.split('\n')
        self.ensure_title(lines)
        corrected_lines = self.normalize_headers(lines)
        return '\n'.join(corrected_lines)
