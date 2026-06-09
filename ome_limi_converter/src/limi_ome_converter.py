'''
This is the code for converting from a LiMi object to an OME object
Parse the LiMi XML file according to the LiMi schema (or devoid of any schema?)
Create an OME object by filling in the appropriate values for elements taken from the LiMi object
Serialize and store the LiMi object within one of the OME object attributes
'''
from limi_validator import *
import xmlschema
import xml.etree.ElementTree as ET
from limi import LiMi
from ome import *
from mapping_csv_conv import *
from ome_types.model import OME, Instrument, Objective


def create_ome_objects():
    # obj = Objective(
    # id="Objective:0",
    # manufacturer="Zeiss",
    # model="Plan-Apochromat",
    # nominal_magnification=63.0,
    # lens_na=1.4,
    # )

    # instrument = Instrument(
    #     id="Instrument:0",
    #     objective=[obj]
    # )

    # ome = OME(
    #     instrument=[instrument]
    # )

    # xml = ome.to_xml()
    # print(xml)
    # ome = OME(
    # instrument=[
    #     Instrument(
    #         id="Instrument:0",
    #         objective=[
    #             Objective(
    #                 id="Objective:0",
    #                 manufacturer="Zeiss",
    #                 model="Plan-Apochromat",
    #                 nominal_magnification=63.0,
    #                 lens_na=1.4,
    #                 )
    #             ],
    #         )
    #     ]
    # )

    # xml_string = ome.to_xml()
    pass

def parse_from_json(
        source: str,
        validate: bool | None,
        ) -> LiMi:
    '''Parses content from a user provided JSON file into a LiMi object

    Parameters
    -------------------------
    source: Path to a JSON file
    validate: Boolean to indicate whether to validate xml file against LiMi schema

    Returns
    -------------------------
    LiMi: a LiMi object parsed from the XML file
    '''
    schema_file = "../fullSchema.json"
    if validate:
        valid = validate_limi(schema_file, source)
        if not valid:
            print("JSON file provided does not follow LiMi schema!")
        else:
            print("valid Json file provided (debugging purposes only)!!")
    with open(source, "r", encoding="utf-8") as df:
        data = json.load(df)
    return data    

def convert_to_ome(
        limi_dict: dict
):
    '''Converts the LiMi object obtained from user provided XML to OME object

    Parameters
    -------------------------
    limi_obj: Original LiMi object obtained from the parsing the XML file

    Returns
    -------------------------
    OME: an OME object converted from the LiMi object
    '''
    root = limi_dict["Schema_ID"].strip(".json")
    if root in all_ome_elements:
        root_ome = all_ome_elements[root]
        print(root_ome.name)
        for comp in limi_dict["components"]:
            schema_id = comp["Schema_ID"].strip(".json")
            if schema_id in all_ome_elements:
                ome_elem = all_ome_elements[schema_id]
                print("     ", ome_elem.name)

def parse_to_xml(
        obj,
        path: str,
        validate: bool | None
) -> bool:
    '''Parses either the OME or LiMi object to XML format

    Parameters
    -------------------------
    obj: a LiMi or OME class object to be parsed to XML format
    path: path to XML file in which to write the object converted to XML
    validate: boolean to indicate whether to validate the resulting XML file

    Returns
    -------------------------
    A Boolean value indicating whether the conversion and writing to XML was successful
    
    '''
    pass

# parse_from_json("C:/Users/riya3/OneDrive - University of Rochester/University of Rochester/UMass Caterina Work/NGM OME project/ome_limi_converter_lib/ome_limi_converter/test/ucsd-ren_lab_basct_nikon_eclipse_ti2-u_scope1.json", True)