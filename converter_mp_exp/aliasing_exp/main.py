from nbo_objective import *
from ome_objective import *
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    # xml_fn_nbo = "nbo_objective.xml"
    # # parse an nbo object from nbo xml file
    # nbo_obj = NBO_Objective.init_from_xml(xml_fn_nbo)
    # # parse an ome objective instance from data in nbo instance
    # ome_obj = nbo_obj.parse_to_ome()
    # # parse ome instance to xml
    # ome_obj.parse_to_xml("nbo_to_ome.xml")

    xml_fn_ome = "ome_objective.xml"
    nbo_data = {}
    nbo_object = NBO_Objective(xml_fn_ome, nbo_data)
    nbo_object.parse_to_xml("nbo_obj_from_ome.xml")
    ome_object = nbo_object.get_ome_obj()
    ome_object.parse_to_xml("ome_obj_from_nbo.xml")

    # parse an ome object from ome xml file
    # ome_obj = OME_Objective.init_from_xml(xml_fn_ome)
    # # parse ome objective instance to nbo instance
    # nbo_obj = ome_obj.parse_to_nbo()
    # # parse nbo object to xml
    # nbo_obj.parse_to_xml("ome_to_nbo.xml")


    