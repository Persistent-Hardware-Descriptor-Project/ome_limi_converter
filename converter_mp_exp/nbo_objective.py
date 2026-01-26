import xml.etree.ElementTree as ET
import xml.dom.minidom
from urllib.parse import quote

class NBO_Objective():

    # There are three types of differences between the core attributes in OME extended into NBO:
    # -1: The attribute does not carry over to nbo object
    # 0: Type Change (cannot safely convert attribute from NBO to OME embedding)
    # 1: Name Change (type and attribute represented are the same, name is different)
    # 2: No Change
    core_attr = {"Manufacturer": ("Manufacturer", 2),
                 "Model": ("Model", 2),
                 "CatalogNumber": ("SerialNumber", 1),
                 "LotNumber": ("LotNumber", 2),
                 "ID": ("ID", 2),
                 "Magnification": ("NominalMagnification", 1),
                 "LensNA": ("LensNA", 2),
                 "Correction": ("Correction", 2),
                 "ImmersionType": ("Immersion", 0),
                 "WorkingDistance": ("WorkingDistance", 2),
                 "WorkingDistanceUnit": ("WorkingDistanceUnit", -1),
                 "CalibratedMagnification": ("CalibratedMagnification", 2),
                 "Iris": ("Iris", 2),
                 "AnnotationRef": ("AnnotationRef", 2)
                 }

    def __init__(self, dd):
        # TODO: type values need to be validated before creating schema instance
        self.derivatives = {"ome": {}}
        self.derivatives["ome"]["Extensions"] = {"nbo": dd}
        self.Manufacturer = dd.get("Manufacturer")
        self.Model = dd.get("Model")
        self.CatalogNumber = dd.get("CatalogNumber")
        self.LotNumber = dd.get("LotNumber")
        self.ID = dd.get("ID")
        self.NominalMagnification = dd.get("NominalMagnification")
        self.LensNA = dd.get("LensNA")
        self.Correction = dd.get("Correction")
        self.ImmersionType = dd.get("ImmersionType")
        self.WorkingDistance = dd.get("WorkingDistance")
        self.Iris = dd.get("Iris")
        self.CalibratedMaginification = dd.get("CalibratedMaginification")
        self.AnnotationRef = dd.get("AnnotationRef")
        self.InfinityCorrected = dd.get("InfinityCorrected")
        self.ContrastModulation = dd.get("ContrastModulation")
        self.DIC = dd.get("DIC")
        self.LightType = dd.get("LightType")
        self.CorrectionCollar = dd.get("CorrectionCollar")
        self.CorrectionCollar_type = dd.get("CorrectionCollarType")
        self.DippingMedium = dd.get("DippingMedium")
        self.PhaseContrastDesignation = dd.get("PhaseContrastDesignation")
        self.ObjectiveViewField = dd.get("ObjectiveViewField")
        self.ImageDistance = dd.get("ImageDistance")
        self.FrontFocalLength = dd.get("FrontFocalLength")
        self.BackFocalLength = dd.get("BackFocalLength")
        self.ParafocalizingDistance = dd.get("ParafocalizingDistance")
        self.derivatives["ome"] = self.extract_ome_data(dd)
        self.derivatives["ome"]["Extensions"] = {"nbo": dd}

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

        core_atts = {}
        for k, v in self.derivatives["ome"].items():
            if k == "Extensions":
                continue
            if v is not None:
                core_atts[k] = v

        nbo_atts = {}
        for attr, val in self.__dict__.items():
            if val is not None:
                nbo_atts[attr] = str(val)

        instrument = ET.SubElement(ome_root, f"{{{ome_ns}}}Instrument", ID="Instrument:0")

        objective = ET.SubElement(instrument, f"{{{ome_ns}}}Objective", attrib=core_atts)
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

    def extract_ome_data(self, dd):
        ome_data = {}
        for k, v in self.core_attr.items():
            if v[1]:
                if k in dd:
                    ome_data[v[0]] = dd[k]
                # ome_data[v[0]] = dd.get(k)
            # else:
                # ome_data[v[0]] = None
        return ome_data

    def parse_to_ome(self):
        from ome_objective import OME_Objective
        ome_obj = OME_Objective(self.derivatives["ome"])
        return ome_obj
    
    def __setattr__(self, attr, val):
        if attr in self.core_attr:
            ome_attr, mode = self.core_attr[attr]
            if mode:
                self.derivatives["ome"][ome_attr] = val
                self.derivatives["ome"]["Extensions"]["nbo"][attr] = val
        object.__setattr__(self, attr, val)