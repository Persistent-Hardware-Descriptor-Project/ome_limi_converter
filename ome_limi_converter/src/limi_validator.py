'''
This program compares the input xml file against the LiMi schema,
to ensure that the file is valid according to the LiMi schema
'''
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema import Draft7Validator


def validate_limi(
        schema_f: str,
        data_f: str
) -> bool:
    '''Function to validate given json data file against json schema file for LiMi objects

    Parameters
    -------------------------
    schema_f: path to json file with LiMi schema
    data_f: path to json file with LiMi object stored

    Returns
    -------------------------
    a boolean value indicating whether the file follows valid LiMi schema or not
    '''
    schema = None
    with open(data_f, "r", encoding="utf-8") as df:
        data = json.load(df)

    with open(schema_f, "r", encoding="utf-8") as sf:
        full_schema = json.load(sf)
        for sc in full_schema:
            if sc["ID"] == data["Schema_ID"]:
                schema = sc

    # print(schema)
    # will only reach the return statement if the validation is passed else raises error
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        return False

    return True


