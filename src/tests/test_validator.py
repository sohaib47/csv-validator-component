# tests/test_validator.py

import os
import json
import pandas as pd
import pytest
from src.csv_validator.schema_loader import SchemaLoader
from src.csv_validator.rules import RequiredRule, TypeRule
from src.csv_validator.validator import Validator

# 1) Test SchemaLoader.load()
def test_schema_loader(tmp_path):
    schema_yml = tmp_path / "schema.yml"
    schema_yml.write_text("""
foo:
  type: integer
  required: true
bar:
  type: string
""".lstrip())
    loaded = SchemaLoader.load(str(schema_yml))
    assert isinstance(loaded, dict)
    assert loaded["foo"]["type"] == "integer"
    assert loaded["foo"]["required"] is True
    assert loaded["bar"]["type"] == "string"

# 2) Test RequiredRule and TypeRule in isolation
def test_rules_individual():
    cfg_req = {"required": True}
    rule_req = RequiredRule("col", cfg_req)
    # missing value
    errs = rule_req.validate("", 5)
    assert errs == ["Row 5: 'col' is required but missing"]
    # present
    assert rule_req.validate("something", 5) == []

    cfg_type = {"type": "integer"}
    rule_type = TypeRule("col", cfg_type)
    # valid
    assert rule_type.validate("123", 7) == []
    # invalid
    errs = rule_type.validate("abc", 7)
    assert errs == ["Row 7: 'col' expected integer but got 'abc'"]

# 3) Test Validator end-to-end on a CSV
def test_validator_end_to_end(tmp_path):
    # Create schema file
    schema = tmp_path / "schema.yml"
    schema.write_text("""
id:
  type: integer
  required: true
name:
  type: string
  required: true
""".lstrip())

    # Create CSV file
    csv = tmp_path / "data.csv"
    df = pd.DataFrame([
        {"id": "1", "name": "Alice"},
        {"id": "",  "name": "Bob"},
        {"id": "xyz","name": ""},
    ])
    df.to_csv(csv, index=False)

    # Run validation
    v = Validator(SchemaLoader.load(str(schema)))
    results = v.validate(str(csv))

    # Expect row 2 missing id, row 3 type error + missing name
    assert 2 in results
    assert "Row 2: 'id' is required but missing" in results[2]
    assert 3 in results
    assert "Row 3: 'id' expected integer but got 'xyz'" in results[3]
    assert "Row 3: 'name' is required but missing" in results[3]

# (Optional) ensure JSON report
def test_json_report(tmp_path):
    errors = {2: ["error one"], 4: ["error two"]}
    prefix = tmp_path / "out"
    from src.csv_validator.reporter import Reporter
    Reporter.write_reports(errors, str(prefix))
    # check JSON
    loaded = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert loaded == errors
    # check HTML exists
    assert (tmp_path / "out.html").exists()
