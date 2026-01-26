import xml.etree.ElementTree as ET
import xml.dom.minidom

class OME_NBO_Objective:

    # There are three types of differences between the core attributes in OME extended into NBO:
    # -1: Unavailable (does not exist in the nbo object)
    # 0: Type Change (cannot safely convert attribute from NBO to OME embenbo_dataing)
    # 1: Name Change (type and attribute represented are the same, name is different)
    # 2: No Change
    # Key is attribute name in OME, value[1] is attribute name in NBO
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

    # xml_fn = filename of the xml file with the ome objective data
    def __init__(self):   
        self.Manufacturer = None
        self.Model = None
        self.SerialNumber = None
        self.LotNumber = None
        self.ID = None
        self.Correction = None
        self.Immersion = None
        self.LensNA = None
        self.NominalMagnification = None
        self.CalibratedMagnification = None
        self.WorkingDistance = None
        self.WorkingDistanceUnit = None
        self.Iris = None
        self.AnnotationRef = None

        self.CatalogNumber = None
        
        self.Magnification = None
        self.ImmersionType = None
        self.InfinityCorrected = None
        self.ContrastModulation = None
        self.DIC = None
        self.LightType = None
        self.CorrectionCollar = None
        self.CorrectionCollar_type = None
        self.DippingMedium = None
        self.PhaseContrastDesignation = None
        self.ObjectiveViewField = None
        self.ImageDistance = None
        self.FrontFocalLength = None
        self.BackFocalLength = None
        self.ParafocalizingDistance = None

        
    def set_nbo_atts(self, nbo_data):
        # sets only attributes that are unique to nbo object
        for key, val in nbo_data.items():
            # Since there are no conditions, this may reset some attributes set by the ome step
            setattr(self, key, val)
        # self.ImmersionType = nbo_data.get("ImmersionType")
        # self.InfinityCorrected = nbo_data.get("InfinityCorrected")
        # self.ContrastModulation = nbo_data.get("ContrastModulation")
        # self.DIC = nbo_data.get("DIC")
        # self.LightType = nbo_data.get("LightType")
        # self.CorrectionCollar = nbo_data.get("CorrectionCollar")
        # self.CorrectionCollar_type = nbo_data.get("CorrectionCollarType")
        # self.DippingMedium = nbo_data.get("DippingMedium")
        # self.PhaseContrastDesignation = nbo_data.get("PhaseContrastDesignation")
        # self.ObjectiveViewField = nbo_data.get("ObjectiveViewField")
        # self.ImageDistance = nbo_data.get("ImageDistance")
        # self.FrontFocalLength = nbo_data.get("FrontFocalLength")
        # self.BackFocalLength = nbo_data.get("BackFocalLength")
        # self.ParafocalizingDistance = nbo_data.get("ParafocalizingDistance")

    def set_ome_atts(self, ome_data):
        # sets ome attribute (also sets atts common between ome and nbo)
        # Create new attributes for class that would work for the ome object
        for key, val in ome_data.items():
            if not val == None:
                setattr(self, key, val)
                
        # If the nbo attr has a different name, give it the val that the ome attr has
        for key, value in ome_data.items():
            if not value == None:
                if key in self.core_attr:
                    if self.core_attr[key][1] == 1:
                        setattr(self, self.core_attr[key][0], value)

        # self.Manufacturer = ome_data.get("Manufacturer")
        # self.Model = ome_data.get("Model")
        # self.SerialNumber = ome_data.get("SerialNumber")
        # self.LotNumber = ome_data.get("LotNumber")
        # self.ID = ome_data["ID"]
        # self.Correction = ome_data.get("Correction")
        # self.Immersion = ome_data.get("Immersion")
        # self.LensNA = ome_data.get("LensNA")
        # self.NominalMagnification = ome_data.get("NominalMagnification")
        # self.CalibratedMagnification = ome_data.get("CalibratedMagnification")
        # self.WorkingDistance = ome_data.get("WorkingDistance")
        # self.WorkingDistanceUnit = ome_data.get("WorkingDistanceUnit")
        # self.Iris = ome_data.get("Iris")
        # self.AnnotationRef = ome_data.get("AnnotationRef")

    def get_nbo_data(self):
        # returns a data dict with all nbo attributes (including those common with ome)
        # ome atts that are not relevant to ome are included in a dict as a separate att
        nbo_atts = {}
        nbo_atts["ome"] = {}
        for attr, val in self.__dict__.items():
            if val is not None:
                if attr in self.core_attr:
                    if self.core_attr[attr][1] != 2:
                        nbo_atts["ome"][attr] = val
                nbo_atts[attr] = str(val)
        return nbo_atts

    def get_ome_data(self):
        # returns a data dict with all ome attribute values
        ome_atts = {}
        for attr, val in self.__dict__.items():
            if val is not None:
                if attr in self.core_attr:
                    ome_atts[attr] = str(val)
        return ome_atts

# can specialize this class to be a builder for specific schema (xml/rdf)
class OME_NBO_Builder:
    def __init__(self, xml_fn, nbo_data, nbo_out_fn, ome_out_fn):
        self.ome_nbo = OME_NBO_Objective()
        self.xml_fn = xml_fn
        self.nbo_data = nbo_data
        self.nbo_out_fn = nbo_out_fn
        self.ome_out_fn = ome_out_fn

    def build_ome(self):
        # calls function to parse xml_fn to ome data dict
        # calls set_ome_atts 
        # calls get_ome_data
        # parses ome to appropriate file format (xml in this case) 
        ome_data = self.parse_xml_to_data(self.xml_fn)
        self.ome_nbo.set_ome_atts(ome_data)
        ome_dict = self.ome_nbo.get_ome_data()
        self.parse_ome_to_xml(ome_dict)

    def build_nbo(self):
        # calls function to set_nbo_atts using nbo data dict
        # calls get_nbo_data to get all atts with their values set
        # parses nbo to appropriate file format (xml in this case)
        self.ome_nbo.set_nbo_atts(self.nbo_data)
        nbo_dict = self.ome_nbo.get_nbo_data()
        self.parse_nbo_to_xml(nbo_dict, self.nbo_out_fn)

    def parse_nbo_to_xml(nbo_atts, out_fn):
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

        instrument = ET.SubElement(ome_root, f"{{{ome_ns}}}Instrument", ID="Instrument:0")

        objective = ET.SubElement(instrument, f"{{{ome_ns}}}Objective", attrib=nbo_atts)
        for key, val in nbo_atts.items():
            child = ET.SubElement(objective, f"{{{nbo_ns}}}{key}")
            child.text = str(val)

        xml_str = ET.tostring(ome_root, encoding="unicode", method="xml")

        dom = xml.dom.minidom.parseString(xml_str)
        indented_str = dom.toprettyxml(indent="  ")
        try:
            with open(out_fn, "w", encoding="utf-8") as outfile:
                outfile.write(indented_str)
        except IOError as e:
            print(f"Error in writing to xml file: {e}")
        pass

    def parse_ome_to_xml(ome_objective, out_fn):
        ns = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'
        ET.register_namespace("", ns)

        ome_root = ET.Element(f"{{{ns}}}OME")

        instrument = ET.SubElement(ome_root, f"{{{ns}}}Instrument", ID = "Instrument:0")

        objective = ET.SubElement(instrument, f"{{{ns}}}Objective", attrib=ome_objective)
        xml_str = ET.tostring(ome_root, encoding="unicode", method="xml")

        dom = xml.dom.minidom.parseString(xml_str)
        indented_str = dom.toprettyxml(indent="  ")
        try:
            with open(out_fn, "w", encoding="utf-8") as outfile:
                outfile.write(indented_str)
        except IOError as e:
            print(f"Error in writing to xml file: {e}")

    def parse_xml_to_ome(xml_fn):
        tree = ET.parse(xml_fn)
        root = tree.getroot()
        ns = {
            'ome': 'http://www.openmicroscopy.org/Schemas/OME/2016-06',
            'nbo': 'https://doi.org/10.5281/zenodo.4711426'
        }
        objective = root.find('.//ome:Objective', ns)

        ome_data = dict(objective.attrib)
        return ome_data


        
    

    
