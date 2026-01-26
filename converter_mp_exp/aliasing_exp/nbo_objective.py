import xml.etree.ElementTree as ET
import xml.dom.minidom
from urllib.parse import quote
from ome_objective import *

class NBO_Objective(OME_Objective):
    
    # nbo_data is a dict that contains data needed to extend the ome object to an nbo object
    # ome_data is another dict containing the parent class data
    def __init__(self, ome_xml, nbo_data):
        # TODO: type values need to be validated before creating schema instance
        print(self.core_attr)
        
        ome_data = self.get_ome_from_xml(ome_xml)
        print(ome_data)
        super().__init__(ome_data)

        self.parent = OME_Objective(ome_data)
        
        # For variables that have a name changed between ome and nbo:
        # create a new variable with the correct name and same value as the ome object
        for key, value in ome_data.items():
            if self.core_attr[key][1] == 1:
                setattr(self, self.core_attr[key][0], value)

        # When initializing the nbo object using a dict, all attributes will need to be included
        # attributes whose values are not currently available can be set to None
        for key, value in nbo_data.items():
            # if the attribute is one of the core ones
            # and the attr is same as the parent attribute (name change included) skip to next iteration 
            if key in self.core_attr:
                mode = self.core_attr[key][1]
                if mode:
                    continue
            # else set a new attribute to have the same name as key and value set to value
            setattr(self, key, value)

    def get_ome_from_xml(self, xml_fn):
        tree = ET.parse(xml_fn)
        root = tree.getroot()
        ns = {
            'ome': 'http://www.openmicroscopy.org/Schemas/OME/2016-06',
            'nbo': 'https://doi.org/10.5281/zenodo.4711426'
        }
        objective = root.find('.//ome:Objective', ns)

        ome_data = dict(objective.attrib)
        return ome_data

    @classmethod
    def init_from_ome(cls, ome):
        nbo_dd = ome.extensions["nbo"]
        nbo_obj = cls(nbo_dd)
        return nbo_obj

    @classmethod
    def init_from_xml(cls, xml_fn):
        tree = ET.parse(xml_fn)
        root = tree.getroot()
        ns = {
            'ome': 'http://www.openmicroscopy.org/Schemas/OME/2016-06',
            'nbo': 'https://doi.org/10.5281/zenodo.4711426'
        }
        objective = root.find('.//ome:Objective', ns)

        ome_data = dict(objective.attrib)
        nbo_fields = {}
        for child in objective.findall('nbo:*', ns):
            tag = child.tag.split('}')[1]
            nbo_fields[tag] = child.text
        
        dd = ome_data | nbo_fields
        nbo_obj = cls(dd)
        return nbo_obj

    # go over core_attrs and directly parse those that are same as ome
    # completely ignore type change ones
    # directly parse all additional attrs (not in the dict)
    # name change ones will be named differently in parent attrs but the value needs to be taken from that   
    def parse_to_xml(self, xml_fn):
        ome_ns = "http://www.openmicroscopy.org/Schemas/OME/2016-06"
        nbo_ns = "https://nbo.github.io/4DN-BINA-OME-Schema"
        xsi_ns = "http://www.w3.org/2001/XMLSchema-instance"
        ET.register_namespace('', ome_ns)
        ET.register_namespace('nbo', nbo_ns)
        ET.register_namespace('xsi', xsi_ns)

        ome_root = ET.Element(f"{{{ome_ns}}}OME", {
            f"{{{xsi_ns}}}schemaLocation":
            f"{{{ome_ns}}} https://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd "
            f"{{{nbo_ns}}}https://zenodo.org/records/4711426/files/NBO_MicroscopyMetadataSpecifications_ALL.xsd"
        })

        nbo_atts = {}
        for attr, val in self.__dict__.items():
            if val is not None:
                if attr in self.core_attr:
                    if self.core_attr[attr][1] != 2:
                        continue
                nbo_atts[attr] = str(val)

        instrument = ET.SubElement(ome_root, f"{{{ome_ns}}}Instrument", ID="Instrument:0")

        objective = ET.SubElement(instrument, f"{{{ome_ns}}}Objective", attrib=nbo_atts)
        for key, val in nbo_atts.items():
            child = ET.SubElement(objective, f"{{{nbo_ns}}}{key}")
            child.text = str(val)

        xml_str = ET.tostring(ome_root, encoding="unicode", method="xml")

        dom = xml.dom.minidom.parseString(xml_str)
        indented_str = dom.toprettyxml(indent="  ")
        try:
            with open(xml_fn, "w", encoding="utf-8") as outfile:
                outfile.write(indented_str)
        except IOError as e:
            print(f"Error in writing to xml file: {e}")
    
    def get_ome_obj(self):
        # return the parent object
        return self.parent