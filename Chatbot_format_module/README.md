# Unified Documentation

The purpose of these modules is to process and convert HTML content into a well-structured Markdown format with correct hierarchical organization. This is essential for implementing a CHATBOT that can effectively process and present structured content.

The Format Module (Formato) is responsible for converting HTML elements into their Markdown equivalents, properly handling tables, code blocks, and other HTML elements to ensure that the content's format is preserved during the transformation.

The Hierarchy Module (Jerarquia), on the other hand, ensures that the converted content has a coherent hierarchical structure, particularly with regard to headers. This module adjusts and normalizes header levels to follow a logical hierarchy, ensuring that the final document is easy to read and well-organized.

Together, these modules facilitate the conversion of HTML content to Markdown, ensuring that both the format and the hierarchical structure are correctly maintained.

## Format Module (Formato)

This module contains various functions and a main class that help process and convert content into different formats.

Init: Initializes an instance of the Format class with the provided content. It also defines a mapping of HTML tags to functions that convert these tags to Markdown format.

Convert_to_md: This function converts HTML content into Markdown format. It uses BeautifulSoup to parse the HTML and iterates over the elements, applying the appropriate conversion according to the tag mapping.

Handle_element: The function processes a specific HTML element and converts it to its Markdown equivalent. It identifies the type of element and applies the appropriate conversion based on the defined tag mapping. If the element is simple text (NavigableString), it cleans it and ensures proper line breaks. If it's an HTML element with a specific tag, it uses the corresponding function from the tag mapping to convert it. It also handles special elements like br, table, and details.

Handle_table: The function converts an HTML table to its equivalent Markdown format. It processes the table headers and body, ensuring that each row and cell is correctly represented in Markdown.

Detect_format: The function analyzes the content to determine its format, specifically HTML, LaTeX, and Markdown (MD), returning a list of detected formats.

Change_chunk: The function processes original content that includes code blocks delimited by quotation marks, changing the code to text and replacing hash signs (#) with comments (//) within those blocks, avoiding conflicts with the hierarchy. It also adds start and end tags to the code block.

## Hierarchy Module (Jerarquia)

This module contains a main class that helps process and normalize the hierarchy of headers in content structured in Markdown.

Init: Initializes an instance of the Hierarchy class with the provided content.

Detect_title: Static method that detects whether the content has a first-level title (#). It scans the content lines and checks if any of them start with #.

Detect_structure: Static method that analyzes the structure of the content's headers. It verifies that the levels of headers (#, ##, ###, etc.) follow a correct hierarchy, starting with a single # and ensuring no levels are skipped.

Create_title_from_content: Static method that creates a first-level title by taking the first 5 words of the content.

Ensure_title: Ensures that the content has a first-level title. If the title is not in the first line of text, it generates a title, even if it detects a title throughout the file, and if there is a subsection on the first line, it converts it into the title.

Normalize_headers: Normalizes the content headers to ensure a correct hierarchy. It adjusts the header levels so that no levels are skipped and corrects improperly hierarchized headers, maintaining a coherent structure.

Correct_structure: Corrects the structure of the content. First, it ensures the content has a title and then normalizes all the headers to maintain a correct hierarchy. It returns the content with the corrected hierarchy.
