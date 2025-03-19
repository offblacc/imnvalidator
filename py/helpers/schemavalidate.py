import json
import jsonschema
import sys
from typing import Tuple

# Does this really need its separate function here?
# I just have it here because I used to run it as main
# So I separated it into a function aswell
def validateJSON(data_file_path: str, schema_file_path: str) -> Tuple[bool, str]:
    with open(data_file_path, 'r') as data_file:
        json_data = json.load(data_file)

    with open(schema_file_path, 'r') as schema_file:
        json_schema = json.load(schema_file)
    try:
        jsonschema.validate(instance=json_data, schema=json_schema)
        return True, 'JSON is valid.'
    except jsonschema.exceptions.ValidationError as err:
        return False, str(err)

def main():
    if len(sys.argv) != 3:
        print("Usage: python schemavalidate.py <data_file_path> <schema_file_path>")
        sys.exit(1)

    data_file_path = sys.argv[1]
    schema_file_path = sys.argv[2]

    # Load the JSON data and schema from files
    with open(data_file_path, 'r') as data_file:
        json_data = json.load(data_file)

    with open(schema_file_path, 'r') as schema_file:
        json_schema = json.load(schema_file)

    # Validate the JSON data against the schema
    try:
        jsonschema.validate(instance=json_data, schema=json_schema)
        print("JSON data is valid.")
    except jsonschema.exceptions.ValidationError as err:
        print("JSON data is invalid:", err)

if __name__ == '__main__':
    main()
