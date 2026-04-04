import os
from typing import List, Dict
from tree_sitter import Parser
from tree_sitter_languages import get_language


class CodeParser:
    def __init__(self, language: str = "python"):
        """
        Initialize Tree-sitter parser
        """
        self.language_name = language
        self.language = get_language(language)
        self.parser = Parser()
        self.parser.set_language(self.language)

    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse a single file and extract functions/classes
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception:
            return []

        tree = self.parser.parse(bytes(code, "utf-8"))
        root_node = tree.root_node

        extracted = []

        self._traverse_tree(root_node, code, extracted, file_path)

        return extracted

    def _traverse_tree(self, node, code: str, extracted: List, file_path: str):
        """
        Recursively traverse AST
        """

        # Python nodes
        if self.language_name == "python":
            if node.type == "function_definition":
                extracted.append(self._extract_node(node, code, file_path, "function"))

            elif node.type == "class_definition":
                extracted.append(self._extract_node(node, code, file_path, "class"))

        # C++ nodes
        elif self.language_name == "cpp":
            if node.type == "function_definition":
                extracted.append(self._extract_node(node, code, file_path, "function"))

            elif node.type == "class_specifier":
                extracted.append(self._extract_node(node, code, file_path, "class"))

        # Traverse children
        for child in node.children:
            self._traverse_tree(child, code, extracted, file_path)

    def _extract_node(self, node, code: str, file_path: str, node_type: str) -> Dict:
        """
        Extract code snippet and metadata
        """
        start_byte = node.start_byte
        end_byte = node.end_byte

        snippet = code[start_byte:end_byte]

        return {
            "type": node_type,
            "file": file_path,
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
            "code": snippet,
        }

    def parse_repository(self, repo_path: str) -> List[Dict]:
        """
        Parse entire repository
        """
        all_data = []

        for root, _, files in os.walk(repo_path):
            for file in files:

                if self._is_valid_file(file):
                    file_path = os.path.join(root, file)
                    parsed = self.parse_file(file_path)
                    all_data.extend(parsed)

        return all_data

    def _is_valid_file(self, filename: str) -> bool:
        """
        Filter relevant files
        """
        extensions = {
            "python": [".py"],
            "cpp": [".cpp", ".hpp", ".h"]
        }

        return any(filename.endswith(ext) for ext in extensions.get(self.language_name, []))