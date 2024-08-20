from bs4 import BeautifulSoup, NavigableString
import re

class Formato:
    def __init__(self, content):
        """
        Initialize with HTML content.
        
        :param content: HTML content to be converted to Markdown.
        """
        self.content = content
        self.tag_mapping = {
            'h1': lambda e: f'# {e.get_text(strip=True)}\n\n',
            'h2': lambda e: f'## {e.get_text(strip=True)}\n\n',
            'h3': lambda e: f'### {e.get_text(strip=True)}\n\n',
            'h4': lambda e: f'#### {e.get_text(strip=True)}\n\n',
            'h5': lambda e: f'##### {e.get_text(strip=True)}\n\n',
            'p': lambda e: ''.join([self.handle_element(child) for child in e.contents]) + '\n\n',
            'ul': lambda e: ''.join([f'- {li.get_text(strip=True)}\n' for li in e.find_all('li')]) + '\n',
            'ol': lambda e: ''.join([f'{idx}. {li.get_text(strip=True)}\n' for idx, li in enumerate(e.find_all('li'), 1)]) + '\n',
            'img': lambda e: f'![{e.get("alt", "").strip()}]({e.get("src", "").strip()})\n\n',
            'div': lambda e: ''.join([self.handle_element(child) for child in e.contents]) + '\n\n',
        }

    def post_process_spacing(self, content):
        content = re.sub(r'(^#+.*?$)', r'\1\n', content, flags=re.MULTILINE)
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r'(?<!^)(\n#+)', r'\n\1', content)
        content = '\n'.join(line.strip() for line in content.split('\n'))
        content = re.sub(r'(^#+.*?\n)\n(#+)', r'\1\2', content, flags=re.MULTILINE)
        return content.strip()
    
    def handle_markdown_with_html(self, content):
        content = re.sub(r'^(#+)\s*<p.*?>(.*?)<\/p>\s*$', self.replace_html_in_header, content, flags=re.MULTILINE)

        # Convert <b>, <i>, <strong>, <em> to Markdown equivalents
        content = re.sub(r'<(strong|b)>(.*?)<\/\1>', r'**\2**', content)
        content = re.sub(r'<(em|i)>(.*?)<\/\1>', r'*\2*', content)
        
        content = re.sub(r'(?<=\n)(#+)', r'\n\1', content)
        return content

    def replace_html_in_header(self, match):
        header_level = len(match.group(1))
        html_content = match.group(2)
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(strip=True)
        return f"{'#' * header_level} {text}\n"

    def convert_to_md(self):
        self.content = self.handle_markdown_with_html(self.content)
        soup = BeautifulSoup(self.content, 'html.parser')
        elements = soup.body.contents if soup.body else soup.contents

        markdown_content = []
        for element in elements:
            markdown_content.append(self.handle_element(element))

        markdown_result = '\n'.join(markdown_content).strip()
        markdown_result = self.post_process_spacing(markdown_result)
        markdown_result = re.sub(r'\n{3,}', '\n\n', markdown_result)
        markdown_result = markdown_result.strip()

        return markdown_result

    def handle_element(self, element):
        if isinstance(element, NavigableString):
            return str(element).strip()
        elif element.name == 'br':
            return '\n'
        elif element.name == 'table':
            return self.handle_table(element)
        elif element.name in self.tag_mapping:
            return self.tag_mapping[element.name](element)
        elif element.name == 'details':
            summary = element.find('summary')
            if summary:
                summary_text = summary.get_text(strip=True)
                details_content = ''.join([self.handle_element(child) for child in element.contents if child != summary])
                return f'{summary_text}\n{details_content}\n\n'
            else:
                return ''.join([self.handle_element(child) for child in element.contents])
        else:
            return ''.join([self.handle_element(child) for child in element.contents])
        
    def handle_table(self, table):
        table_md = ''
        
        rows = table.find_all('tr')
        if not rows:
            return ''
        
        header_cells = rows[0].find_all(['th', 'td'])
        if header_cells:
            table_md += '| ' + ' | '.join(cell.get_text(strip=True) for cell in header_cells) + ' |\n'
            table_md += '| ' + ' | '.join('---' for _ in header_cells) + ' |\n'
        
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            table_md += '| ' + ' | '.join(cell.get_text(strip=True) for cell in cells) + ' |\n'
        
        return table_md.strip() + '\n\n'


    
    def detect_format(self):
        detected_formats = []

        html_tags = ['<!DOCTYPE html>', '<html>', '<div', '<h1', '<p', '<br', '<table']
        if any(re.search(tag, self.content, re.IGNORECASE) for tag in html_tags):
            detected_formats.append('html')

        if re.search(r'\\begin{document}', self.content, re.IGNORECASE):
            detected_formats.append('latex')

        md_patterns = [r'#\s', r'\n##\s', r'\n###\s', r'!\[.*?\]\(.*?\)', r'\[.*?\]\(.*?\)', r'\*\*.*?\*\*']
        if any(re.search(pattern, self.content, re.MULTILINE) for pattern in md_patterns):
            detected_formats.append('md')

        return detected_formats if len(detected_formats) > 1 else detected_formats[0] if detected_formats else None


    def change_chunk(self):
        parts = self.content.split("```")
        
        new_content = []
        
        for i, part in enumerate(parts):
            if i % 2 == 1:  
                part = part.replace("#", "// ")
                new_content.append("Comienzo del bloque de código: \n")
                new_content.append(part)
                new_content.append("\nFin del bloque de código")
            else:  
                new_content.append(part)
        
        modified_content = ''.join(new_content)
        
        return modified_content
