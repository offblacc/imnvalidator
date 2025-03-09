import json
import jsonschema

# Load the JSON data and schema from files
with open('../../testfiles/tests.json', 'r') as data_file:
    json_data = json.load(data_file)

with open('../../test_file_schema.json', 'r') as schema_file:
    json_schema = json.load(schema_file)

# Validate the JSON data against the schema
try:
    jsonschema.validate(instance=json_data, schema=json_schema)
    print("JSON data is valid.")
except jsonschema.exceptions.ValidationError as err:
    print("JSON data is invalid:", err)
