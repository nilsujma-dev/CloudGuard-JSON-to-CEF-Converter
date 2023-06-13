import os
import json
import shutil
from genson import SchemaBuilder

def get_schema(json_obj):
    builder = SchemaBuilder()
    builder.add_object(json_obj)
    return builder.to_schema()

def write_schema_to_file(schema, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(schema, f, indent=4)
        print(f'Schema has been written to {file_path}')
    except Exception as e:
        print(f"Error while writing schema to file: {e}")

def create_dir(dir_path):
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        print(f"Error while creating directory: {e}")

def process_files(dir_path):
    schemas = []
    schema_dirs = []
    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(dir_path, filename), 'r') as f:
                    data = json.load(f)
                schema = get_schema(data)

                if schema in schemas:
                    index = schemas.index(schema)
                    shutil.copy(os.path.join(dir_path, filename), schema_dirs[index])
                else:
                    schemas.append(schema)
                    new_dir = os.path.join(dir_path, f'schema_dir_{len(schemas)}')
                    create_dir(new_dir)
                    schema_dirs.append(new_dir)
                    shutil.copy(os.path.join(dir_path, filename), new_dir)
                    write_schema_to_file(schema, os.path.join(new_dir, 'schema.json'))
            except Exception as e:
                print(f"Error while reading file: {e}")

dir_path = '/home/nils/dev/github/dome9-webhook-examples/examples'  # change this to your json files directory
process_files(dir_path)

