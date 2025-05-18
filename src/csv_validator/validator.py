# src/csv_validator/validator.py

import pandas as pd
from .rules import RequiredRule, TypeRule, RangeRule, RegexRule

class Validator:
    """Applies schema rules and uniqueness checks to a CSV."""

    def __init__(self, schema: dict):
        self.schema = schema
        self.rules = []
        for col, cfg in schema.items():
            if cfg.get("required", False):
                self.rules.append(RequiredRule(col, cfg))
            if "type" in cfg:
                self.rules.append(TypeRule(col, cfg))
            if "minimum" in cfg or "maximum" in cfg:
                self.rules.append(RangeRule(col, cfg))
            if "pattern" in cfg:
                self.rules.append(RegexRule(col, cfg))

    def validate(self, csv_path: str) -> dict[int, list[str]]:
        df = pd.read_csv(csv_path, dtype=str)
        errors: dict[int, list[str]] = {}

        # Per-row checks (row.get returns None for missing columns)
        for idx, row in df.iterrows():
            row_num = idx + 2
            row_errs: list[str] = []
            for rule in self.rules:
                val = row.get(rule.column)
                row_errs.extend(rule.validate(val, row_num))
            if row_errs:
                errors[row_num] = row_errs

        # Uniqueness checks (skip columns not present)
        for col, cfg in self.schema.items():
            if not cfg.get("unique", False):
                continue
            if col not in df.columns:
                # Optionally: record an overall error about missing column
                # errors.setdefault(1, []).append(f"Column '{col}' not found for uniqueness check")
                continue

            # only non-empty values
            series = df[col].dropna().loc[lambda s: s != ""]
            dupes = series[series.duplicated(keep=False)]
            for idx in dupes.index:
                row_num = idx + 2
                val = df.at[idx, col]
                msg = f"Row {row_num}: '{col}' has duplicate value '{val}'"
                errors.setdefault(row_num, []).append(msg)

        return errors
