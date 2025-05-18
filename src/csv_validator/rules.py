import pandas as pd
import re
from datetime import datetime

class Rule:
    """Base class for validation rules."""
    def __init__(self, column: str, config: dict):
        self.column = column
        self.config = config

    def validate(self, value, row_number: int) -> list[str]:
        raise NotImplementedError

class RequiredRule(Rule):
    """Ensures a required column is not empty or NaN."""
    def validate(self, value, row_number: int) -> list[str]:
        errors = []
        if self.config.get("required", False):
            if value is None or (isinstance(value, float) and pd.isna(value)) \
               or (isinstance(value, str) and value.strip() == ""):
                errors.append(f"Row {row_number}: '{self.column}' is required but missing")
        return errors

class TypeRule(Rule):
    """Checks that a value matches the declared type."""
    def validate(self, value, row_number: int) -> list[str]:
        errors = []
        if value is None or (isinstance(value, float) and pd.isna(value)) or value == "":
            return errors
        typ = self.config.get("type")
        try:
            if typ == "integer":
                int(value)
            elif typ == "number":
                float(value)
            elif typ == "date":
                fmt = self.config.get("format", "%Y-%m-%d")
                datetime.strptime(value, fmt)
        except Exception:
            errors.append(f"Row {row_number}: '{self.column}' expected {typ} but got '{value}'")
        return errors

class RangeRule(Rule):
    """Validates numeric ranges (minimum/maximum)."""
    def validate(self, value, row_number: int) -> list[str]:
        errors = []
        if value is None or value == "" or (isinstance(value, float) and pd.isna(value)):
            return errors
        num = float(value)
        mn = self.config.get("minimum")
        if mn is not None and num < mn:
            errors.append(f"Row {row_number}: '{self.column}' below minimum {mn} (got {value})")
        mx = self.config.get("maximum")
        if mx is not None and num > mx:
            errors.append(f"Row {row_number}: '{self.column}' above maximum {mx} (got {value})")
        return errors

class RegexRule(Rule):
    """Validates string against a regex pattern."""
    def validate(self, value, row_number: int) -> list[str]:
        errors = []
        pattern = self.config.get("pattern")
        if not pattern or value is None or (isinstance(value, str) and value.strip() == ""):
            return errors
        if not re.match(pattern, value):
            errors.append(f"Row {row_number}: '{self.column}' does not match pattern")
        return errors
