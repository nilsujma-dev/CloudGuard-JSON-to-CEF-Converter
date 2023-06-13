import os
import json
from genson import SchemaBuilder
from pprint import pprint

def get_schema(json_obj):
    builder = SchemaBuilder()
    builder.add_object(json_obj)
    schema = builder.to_schema()
    return schema

def write_schema_to_file(schema, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=4)
        print(f'Schema has been written to {file_path}')
    except Exception as e:
        print(f"Error while writing schema to file: {e}")

def compare_schemas(dir_path):
    schemas = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(dir_path, filename), 'r') as f:
                    data = json.load(f)
                schema = get_schema(data)
                if schema not in schemas:
                    schemas.append(schema)
            except Exception as e:
                print(f"Error while reading file: {e}")

    # Assuming the comparison you want to make is whether all schemas are the same
    if len(schemas) > 1:
        print("Schemas are not identical.")
    else:
        print("All json files have identical schemas.")
        schema_file = 'schema.json'
        write_schema_to_file(schemas[0], schema_file)

dir_path = '/home/nils/dev/github/dome9-webhook-examples/examples'  # change this to your json files directory
compare_schemas(dir_path)

