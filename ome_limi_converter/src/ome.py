from __future__ import annotations
from enum import Enum

class XSD_types(Enum):
    string = "xsd:string"
    boolean = "xsd:boolean"
    decimal = "xsd:decimal"
    float = "xsd:float"
    double = "xsd_double"
    b64_binary = "xsd:base64Binary"
    hex_binary = "xsd:hexBinary"
    uri = "xsd:anyURI"
    int = "xsd:int"
    long = "xsd:long"


class OME_complex_type:
    def __init__(self,
                name: str,
                type_: str
                ):
        '''class to create new OME types

        Parameters
        -------------------------
        name: name of the OME type
        type_: simple or complex type

        Returns
        -------------------------
        an object of type OME_complex_type
        '''
        self.name = name
        self.type_ = type_
        self.ext = None
        self.global_ = False
        self.elements = []
        self.attributes = []

    
    
    

class OME_attribute:
    def __init__(self,
                 name: str,
                 type_: OME_complex_type | XSD_types,
                 rest: OME_complex_type | XSD_types):
        '''class to create new OME attributes

        Parameters
        -------------------------
        name: name of the attribute
        type_: type of the attribute
        rest: restriction type

        Returns
        -------------------------
        an object of type OME_attribute
        '''
        self.name = name
        self.type = type_
        self.rest = rest

class OME_element:
    def __init__(self, 
                name: str,
                type_: str,
                ):
        '''class to create new OME elements

        Parameters
        -------------------------
        name: name of the OME global element
        type_: overall type of the element if any (can be simple, complex or xsd type)

        Returns
        -------------------------
        an object of type OME_element
        '''
        self.name = name
        self.type_ = type_
        self.ext = None
        self.rest = None
        self.global_ = False
        # nested elements include local elements and references to global elements
        self.nested_elements = []
        self.attributes = []

    def serializer():
        pass

