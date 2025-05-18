
# CSV Validator Component

A schema-driven CSV validation CLI that produces both HTML and JSON error reports.

## Installation

Install from PyPI in one step:

bash
pip install csv-validator-component


## Usage

Validate any CSV against your schema and write reports:

```bash
csv-validator \
  --csv path/to/data.csv \
  --schema path/to/schema/example_schema.yml \
  --report report_prefix


This will generate:

report_prefix_data.html — an HTML table of all validation errors
report_prefix_data.json — the same errors in JSON format

That’s it: one install command, one CLI command, and your reports are ready.


Simply replace the placeholder text in the GitHub editor with the block above, commit, and you’ll have clear, concise instructions for any user to install and run your component.

