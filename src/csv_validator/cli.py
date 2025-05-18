import json
import click
from .schema_loader import SchemaLoader
from .validator import Validator
from .reporter import Reporter

@click.command()
@click.option(
    '--csv', 'csv_path', required=True,
    help='Path to the CSV file to validate'
)
@click.option(
    '--schema', 'schema_path', required=True,
    help='Path to the YAML/JSON schema file'
)
@click.option(
    '--report', 'report_prefix', required=False,
    help='Prefix for output report files (JSON + HTML)'
)
def main(csv_path, schema_path, report_prefix):
    """
    Validate a single CSV against a schema and generate reports.
    """
    # Load and validate schema
    schema = SchemaLoader.load(schema_path)

    # Run validation
    errors = Validator(schema).validate(csv_path)

    # Output
    if report_prefix:
        # e.g. test_report_data.html/json
        base = f"{report_prefix}_{csv_path.rsplit('.',1)[0]}"
        Reporter.write_reports(errors, base)
        click.echo(f"Reports written to:\n  HTML: {base}.html\n  JSON: {base}.json")
    else:
        click.echo(json.dumps(errors or {"message": "No errors found"}, indent=2))

if __name__ == '__main__':
    main()
