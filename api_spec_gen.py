import json
import yaml


def infer_type(value):
    """Infer the JSON schema type for a given Python value."""
    if isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'number'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, list):
        return 'array'
    elif isinstance(value, dict):
        return 'object'
    else:
        return 'string'  # Default to string if type is unknown

def generate_api_spec_from_json(data, yaml_file_path):

    # Define a basic API specification structure
    api_spec = {
        'openapi': '3.0.0',
        'info': {
            'title': 'Generated API',
            'version': '1.0.0',
            'description': 'API generated from a JSON file.'
        },
        'paths': {},
        'components': {
            'schemas': {}
        }
    }

    # Example of adding paths and components based on JSON keys
    # Generate paths and components based on JSON keys
    for key, value in data.items():
        if isinstance(value, list) and value:
            item_type = key.rstrip('s').capitalize()  # Simplistic singularization and capitalization
            api_spec['paths'][f'/{key}'] = {
                'get': {
                    'summary': f'List {key}',
                    'responses': {
                        '200': {
                            'description': f'Array of {item_type}',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'array',
                                        'items': {
                                            '$ref': f'#/components/schemas/{item_type}'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            # Infer the schema for the item based on the first item in the list
            properties = {}
            for prop_key, prop_value in value[0].items():
                properties[prop_key] = {'type': infer_type(prop_value)}
                if isinstance(prop_value, list):
                    # Assuming a list of simple types (e.g., strings) for simplicity
                    properties[prop_key]['items'] = {'type': 'string'}

            api_spec['components']['schemas'][item_type] = {
                'type': 'object',
                'properties': properties
            }

    # Write the API specification to a YAML file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(api_spec, yaml_file, allow_unicode=True, default_flow_style=False)


# Example usage
json_file_path = '5.json'
yaml_file_path = 'api_spec.yml'

# Load JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

generate_api_spec_from_json(data, yaml_file_path)
