import xml.etree.ElementTree as ET
import xml.dom.minidom

class OME_Objective:
    # -1: Attribute does not exist in LiMi schema
    # 0: Type Change (cannot safely convert attribute from NBO to OME embedding)
    # 1: Name Change (type and attribute represented are the same, name is different)
    # 2: No Change
    core_attr = {"Manufacturer": ("Manufacturer", 2),
                 "Model": ("Model", 2),
                 "SerialNumber": ("CatalogNumber", 1),
                 "LotNumber": ("LotNumber", 2),
                 "ID": ("ID", 2),
                 "NominalMagnification": ("Magnification", 1),
                 "LensNA": ("LensNA", 2),
                 "Correction": ("Correction", 2),
                 "Immersion": ("ImmersionType", 0),
                 "WorkingDistance": ("WorkingDistance", 2),
                 "WorkingDistanceUnit": ("WorkingDistanceUnit", -1),
                 "CalibratedMagnification": ("CalibratedMagnification", 2),
                 "Iris": ("Iris", 2),
                 "AnnotationRef": ("AnnotationRef", 2)
                 }

    # dd = data dict to fill out values from
    def __init__(self, dd):
        try:
            self.Extensions = {"nbo": {}}
            self.Extensions["nbo"]["derivatives"] = {"ome": dd}
            self.Manufacturer = dd.get("Manufacturer")
            self.Model = dd.get("Model")
            self.SerialNumber = dd.get("SerialNumber")
            self.LotNumber = dd.get("LotNumber")
            self.ID = dd["ID"]
            self.Correction = dd.get("Correction")
            self.Immersion = dd.get("Immersion")
            self.LensNA = dd.get("LensNA")
            self.NominalMagnification = dd.get("NominalMagnification")
            self.CalibratedMagnification = dd.get("CalibratedMagnification")
            self.WorkingDistance = dd.get("WorkingDistance")
            self.WorkingDistanceUnit = dd.get("WorkingDistanceUnit")
            self.Iris = dd.get("Iris")
            self.AnnotationRef = dd.get("AnnotationRef")
            self.Extensions["nbo"] = self.extract_nbo_data(dd)
            self.Extensions["nbo"]["derivatives"] = {"ome": dd}
        except KeyError:
            print("Missing OME required field")
    
    @classmethod
    def init_from_xml(cls, xml_fn):
        xml_fn = "nbo_objective.xml"
        tree = ET.parse(xml_fn)
        root = tree.getroot()
        ns = {
            'ome': 'http://www.openmicroscopy.org/Schemas/OME/2016-06',
            'nbo': 'https://doi.org/10.5281/zenodo.4711426'
        }
        objective = root.find('.//ome:Objective', ns)

        ome_data = dict(objective.attrib)
        ome_obj = cls(ome_data)
        return ome_obj

    def parse_to_xml(self, xml_fn):
        ns = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'
        ET.register_namespace("", ns)

        ome_root = ET.Element(f"{{{ns}}}OME")

        instrument = ET.SubElement(ome_root, f"{{{ns}}}Instrument", ID = "Instrument:0")

        ome_objective = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                ome_objective[attr] = str(value)

        objective = ET.SubElement(instrument, f"{{{ns}}}Objective", attrib=ome_objective)
        xml_str = ET.tostring(ome_root, encoding="unicode", method="xml")

        dom = xml.dom.minidom.parseString(xml_str)
        indented_str = dom.toprettyxml(indent="  ")
        try:
            with open(xml_fn, "w", encoding="utf-8") as outfile:
                outfile.write(indented_str)
        except IOError as e:
            print(f"Error in writing to xml file: {e}")

    def extend_to_nbo(self, nbo_dd):
        # How should users be allowed to extend an ome object to an nbo object
        # Users need to pass a dict with NBO field values?
        # Set each NBO attribute individually? (will need to define a dict with NBO extension attributes)
        # 
        print("nbo")

    def extract_nbo_data(self, dd):
        nbo_data = {}
        for k, v in self.core_attr.items():
            if v[1]:
                if k in dd:
                    nbo_data[v[0]] = dd[k]
                    # nbo_data[v[0]] = dd.get(k)
            # else:
            #     nbo_data[v[0]] = None
        return nbo_data
        
    def parse_to_nbo(self):
        from nbo_objective import NBO_Objective
        nbo_obj = NBO_Objective(self.Extensions["nbo"])
        return nbo_obj

    def __setattr__(self, attr, val):
        if attr in self.core_attr:
            nbo_attr, mode = self.core_attr[attr]
            if mode:
                self.Extensions["nbo"][nbo_attr] = val
                self.Extensions["nbo"]["derivatives"]["ome"][attr] = val
        object.__setattr__(self, attr, val)

    

    

    
