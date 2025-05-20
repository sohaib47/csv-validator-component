````markdown
# CSV Validator Component

A **schema-driven** Python CLI & library for validating CSV files and producing both human-readable HTML and machine-readable JSON reports.

## Features

- **Declarative Schemas**  
  Define your validation rules in a simple YAML or JSON file (required fields, data types, ranges, regex patterns, uniqueness).

- **Single or Multi-CSV Validation**  
  Validate one or more CSVs in a single command with `--csv` (repeatable) or by pointing `--dir` at a folder of `.csv` files.

- **Dual-Format Reporting**  
  Generates:
  - `*.json` — structured error data  
  - `*.html` — styled table with sticky headers and hover highlights  

- **Pluggable Rules Engine**  
  Easily extend by subclassing the `Rule` base class in **`src/csv_validator/rules.py`**.

- **Minimal Dependencies**  
  Only `pandas`, `PyYAML`, `click`, and `jinja2`.

- **Editable Install & CLI**  
  Install locally in “editable” mode for development, or publish on PyPI for one-line installs.

## Installation

### From PyPI

```bash
pip install csv-validator-component
````

### From Source (Editable)

```bash
git clone https://github.com/sohaib47/csv-validator-component.git
cd csv-validator-component
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Quick Start

1. **Create a schema** (`schema/example_schema.yml`):

   ```yaml
   emp_id:
     type: integer
     required: true
     unique: true

   name:
     type: string
     required: true
   ```

2. **Run validation**:

   ```bash
   csv-validator \
     --csv data.csv \
     --schema schema/example_schema.yml \
     --report report_output
   ```

3. **Inspect reports**:

   * `report_output_data.html`
   * `report_output_data.json`

## Usage Examples

### Single CSV

```bash
csv-validator \
  --csv data.csv \
  --schema schema/example_schema.yml \
  --report report1
```

### Multiple CSVs

```bash
csv-validator \
  --csv data1.csv \
  --csv data2.csv \
  --schema schema/example_schema.yml \
  --report multi_report
```

### Directory Mode

```bash
csv-validator \
  --dir datasets/ \
  --schema schema/example_schema.yml \
  --report batch_report
```

## Schema Definition

Your schema maps columns to rule configurations:

```yaml
column_name:
  required: true           # boolean
  type: integer            # integer | number | date | string
  format: "%Y-%m-%d"       # for date
  minimum: 0               # for number
  maximum: 100             # for number
  pattern: "^[A-Z]{3}-\\d+$" # regex for string
  unique: true             # enforce uniqueness
```

## Extending Rules

1. Open **`src/csv_validator/rules.py`**.
2. Subclass `Rule` and implement `validate(self, value, row_number) → list[str]`.
3. Register your new rule in **`Validator.__init__`**.

## Running Tests

```bash
pip install pytest
pytest -q
```

## License

MIT © 2025 [sohaib47](https://github.com/sohaib47)


