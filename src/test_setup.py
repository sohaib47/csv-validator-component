from src.csv_validator.schema_loader import SchemaLoader
import json

schema = SchemaLoader.load('schema/example_schema.yml')
print(json.dumps(schema, indent=2))
