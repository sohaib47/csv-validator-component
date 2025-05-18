import os
import yaml
import json

class SchemaLoader:
    """Loads and validates a YAML or JSON schema file."""

    @staticmethod
    def load(path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Schema file not found: {path}")
        ext = os.path.splitext(path)[1].lower()
        with open(path, 'r', encoding='utf-8') as f:
            if ext in ('.yaml', '.yml'):
                schema = yaml.safe_load(f)
            elif ext == '.json':
                schema = json.load(f)
            else:
                raise ValueError(f"Unsupported schema extension: {ext}")
        if not isinstance(schema, dict):
            raise TypeError("Schema must be a top-level mapping (dict).")
        return schema
