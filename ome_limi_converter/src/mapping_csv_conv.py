import pandas as pd
import xmlschema
import xml.etree.ElementTree as ET
from ome import *

all_ome_elements = {}
all_ome_cts = {}
# attributes are only being tracked for debugging and finding mistakes in the csv file
all_ome_attributes = []
count = 0

# TODO: create a global simple types dict as well (no need for a recursive traversal function for this)

def csv_to_dict(filename):
    '''Parses a csv file into a mapping of how limi objects convert to ome objects
        (csv file is included with the library)

    Parameters
    -------------------------
    filename: name of the csv file 

    Returns
    -------------------------
    a python dict with limi element names as keys and ome elements that they map to as values
    '''

    df = pd.read_csv(filename)

    data_dict = df.to_dict(orient='records')
    # print(data_dict)
    # print("--- DEBUGGING INDEX ISSUE ---")
    # for i in range(len(data_dict)):
    #     if any("removed" in str(k) for k in data_dict[i].values()):
    #         print(i, "      ", data_dict[i])

    # change variable name
    prev_j = 7
    prev_elem = ""
    limi_elems = {}
    parent_stack = []

    for i in range(len(data_dict)):
        row = data_dict[i]
        non_nan_row = False

        if all(pd.isna(x) for x in row.values()):
            continue

        for j in range(1, 7):
            if not pd.isna(row[str(j)]):
                non_nan_row = True
                break

        if not non_nan_row:
            continue

        curr_elem = row[str(j)]
        in_ome = row['OME 6-2016']
        ome_dtype = row['OME Data type']

        if curr_elem == "removed OME field(s)":
            curr_elem = parent_stack[-1][0] + "_rmf"
            limi_elems[curr_elem] = ([in_ome], in_ome, ome_dtype)
            i += 1
            rmf_row = data_dict[i]
            while (all(pd.isna(rmf_row[str(x)]) for x in range(1, 7))) and not pd.isna(rmf_row["OME 6-2016"]):
                in_ome = rmf_row["OME 6-2016"]
                limi_elems[curr_elem][0].append(in_ome)
                i += 1
                rmf_row = data_dict[i]
            continue

        else:
            limi_elems[curr_elem] = ([], in_ome, ome_dtype)
            if j > prev_j:
                limi_elems[prev_elem][0].append(curr_elem)
                parent_stack.append((prev_elem, prev_j))
            
            elif j < prev_j:
                while len(parent_stack) and parent_stack[-1][1]>= j:
                    parent_stack.pop()
                if len(parent_stack) != 0:
                    curr_parent = parent_stack[-1][0]
                    limi_elems[curr_parent][0].append(curr_elem)

            else:
                if len(parent_stack) != 0:
                    curr_parent = parent_stack[-1][0]
                    limi_elems[curr_parent][0].append(curr_elem)

            prev_j = j
            prev_elem = curr_elem

    # print(limi_elems)
    return limi_elems                
    # iterate over the csv file row by row
    # go over all the columns and find the first non nan value in the dict
    # if the col num of non nan val for current row > col num of non nan val for prev row:
    #       add val of curr row to list of elements for val of prev row
    #       add val of prev row to the top of parent stack
    # if column num of non nan val for current row < col num of non nan val for prev row:
    #       pop parents off stack until the col num of parent on stack matches that of the curr row's elem
    #       then pop that parent off the stack as well
    #       now add the current element to the list of the elem at the top of the stack
    #       if no element on top of stack then add the element directly to the dict (since this is a top level element)
    # else:
    #       add the current element to the list of the element on the top of the parent stack
    #       if no element on the top of the stack, then add element directly to the dict (top level element)


def xsd_to_ome(ome_xsd_loc = "../ome.xsd"):
    '''Creates an abstraction of the ome xsd in code for quick lookup when converting limi to ome

    Parameters
    -------------------------
    ome_xsd_loc: location of the ome xsd (by default assume it is in src folder)

    Returns
    -------------------------
    Nothing; populates global all_ome_elems and all_ome_cts dicts
    '''

    tree = ET.parse(ome_xsd_loc)
    root = tree.getroot()

    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    schema = xmlschema.XMLSchema(ome_xsd_loc)
    
    global_elem = {}
    for elem in root.findall("./xs:element", ns):
        name = elem.attrib.get("name")
        if name:
            global_elem[name] = elem
            # TODO: create objects from the elements and add to another dict
            # or should i have all elements stored like this in the dict and use python functions to get specific values that I need???
    
    global_cts = {}
    for ct in root.findall("./xs:complexType", ns):
        name = ct.attrib.get("name")
        if name:
            global_cts[name] = ct

    for elem in root.findall("./xs:element", ns):
        traverse_elements(elem, ns, global_elem, global_cts)

    for ct in root.findall("./xs:complexType", ns):
        traverse_complex_types(ct, ns, global_elem, global_cts)

    # --- Stuff for Debugging ---

    # print(count)
    # for k in sorted(all_ome_elements):
    #     if all_ome_elements[k].rest:
    #         print(k, "      ", all_ome_elements[k].rest)
    #     elif all_ome_elements[k].ext:
    #         print(k, "      ", all_ome_elements[k].ext)
    #     else:
    #         print(k)
    #     for att in all_ome_elements[k].attributes:
    #         print("      @", att.name)
    #     for elem in all_ome_elements[k].nested_elements:
    #         print("     <>", elem)

    # print("---Printing Complex Types---")
    # for c in sorted(all_ome_cts):
    #     if all_ome_cts[c].ext:
    #         print(c, "      ", all_ome_cts[c].ext)
    #     else:
    #         print(c)
    #     for elem in all_ome_cts[c].elements:
    #         print("     <>", elem)
    #     for att in all_ome_cts[c].attributes:
    #         print("     @", att)

    # print(global_cts)

def traverse_elements(elem, ns, global_elements, global_cts, root=None):
    '''Recursively traverses elements in ome xsd to create OME_element objects and store them in dict 

    Parameters
    -------------------------
    elem: root element from where to start traversal
    ns: namespace
    global_elements: dict of all global ome elements (key = element names; values = xml etree objects)
    global_cts: dict of all global ome complex types

    Returns
    -------------------------
    Nothing; populates global all_ome_elems dict
    '''

    global all_ome_elements
    global count

    name = elem.attrib.get("name")
    ref = elem.attrib.get("ref")
    type_ = elem.attrib.get("type")

    ome_elem = OME_element(name, type_)
    if name in global_elements:
        ome_elem.global_ = True

    if ref:
        if ref in global_elements:
            traverse_elements(global_elements[ref], ns, global_elements, global_cts)
        return

    if name:
        complex_type = elem.find("xs:complexType", ns)
        if complex_type is not None:
            ext = complex_type.find(".//xs:extension", ns)
            if ext is not None:
                ome_elem.ext = ext.attrib.get("base")
            nelements = complex_type.findall(".//xs:element", ns)
            for nel in nelements:
                nel_name = nel.attrib.get("name")
                nel_ref = nel.attrib.get("ref")
                if nel_name is not None:
                    if nel_name not in all_ome_elements:
                        traverse_elements(nel, ns, global_elements, global_cts, root=name)
                    ome_elem.nested_elements.append(nel_name)
                elif nel_ref is not None:
                    ome_elem.nested_elements.append(nel_ref)
                # TODO: Should the following code be nested in the for loop that iterates over the nested elements
                # Doesn't this code just change the restriction of the root ome element based on the simple type restriction of the nested element?
                st = nel.find("xs:simpleType", ns)
                if st is not None:
                    rest = st.find("xs:restriction", ns).attrib.get("base")
                    if rest is not None:
                        ome_elem.rest = rest
            nattributes = complex_type.findall(".//xs:attribute", ns)
            for nattr in nattributes:
                nattr_name = nattr.attrib.get("name")
                nattr_type = nattr.attrib.get("type")
                st = nattr.find("xs:simpleType", ns)
                rest = None
                if st is not None:
                    rest = st.find("xs:restriction", ns)
                all_ome_attributes.append(nattr_name)
                ome_attr = OME_attribute(nattr_name, nattr_type, rest)
                ome_elem.attributes.append(ome_attr)
            traverse_complex_types(complex_type, ns, global_elements, global_cts)

    # Case 4: Inline simple type
    simple_type = elem.find("xs:simpleType", ns)
    if simple_type is not None:
        rest = simple_type.find("xs:restriction", ns).attrib.get("base")
        ome_elem.rest = rest
    
    if name is not None:
        if root is not None:
            name = name + "_" + root
        all_ome_elements[name] = ome_elem

def traverse_complex_types(ct, ns, global_elements, global_cts):
    '''Recursively traverses complex types in ome xsd to create OME_complex_type objects and store them in dict 

    Parameters
    -------------------------
    ct: root complex type from where to start traversal
    ns: namespace
    global_elements: dict of all global ome elements (key = element names; values = xml etree objects)
    global_cts: dict of all global ome complex types

    Returns
    -------------------------
    Nothing; populates global all_ome_cts dict
    '''
    global all_ome_cts

    name = ct.attrib.get("name")
    type_ = ct.attrib.get("type")

    if name is not None:
        ct_obj = OME_complex_type(name, type_)

        if name in global_cts:
            ct_obj.global_ = True

        seq = ct.find(".//xs:sequence", ns)
        if seq is not None:
            for child in seq.findall(".//xs:element", ns):
                elem_name = child.attrib.get("name")
                elem_ref = child.attrib.get("ref")
                if elem_name is not None:
                    ct_obj.elements.append(elem_name)
                elif elem_ref is not None:
                    ct_obj.elements.append(elem_ref)
                traverse_elements(child, ns, global_elements, global_cts)
        
        # for attributes that are not nested deep
        for attr in ct.findall("xs:attribute", ns):
            attr_name = attr.attrib.get("name")
            if attr_name is not None:
                ct_obj.attributes.append(attr_name)
                all_ome_attributes.append(attr_name)

        cc = ct.find(".//xs:complexContent", ns)
        if cc is not None:
            for attr in cc.findall(".//xs:attribute", ns):
                attr_name = attr.attrib.get("name")
                if attr_name is not None:
                    ct_obj.attributes.append(attr_name)

        # for attributes nested in complex content (not using .// to avoid capturing attrubutes of nested elements)
        cc = ct.find("xs:complexContent", ns)
        if cc is not None:
            ext = cc.find("xs:extension", ns)
            if ext is not None:
                # print("Extension in: ", name)
                base = ext.attrib.get("base")
                ct_obj.ext = base

        all_ome_cts[name] = ct_obj
    
    else:
        choice = ct.find("xs:choice", ns)
        if choice is not None:
            for child in choice.findall("xs:element", ns):
                traverse_elements(child, ns, global_elements, global_cts)
        
        seq = ct.find("xs:sequence", ns)
        if seq is not None:
            for child in seq.findall("xs:element", ns):
                traverse_elements(child, ns, global_elements, global_cts)


limi_elems = csv_to_dict("limi_ome_mapping_simplified.csv")
xsd_to_ome()

# print(all_ome_cts)

def _limi_ome_conv_debugger(limi_elems):
    for elem, tuple in limi_elems.items():
        if not pd.isna(tuple[1]) and elem not in all_ome_elements and elem not in all_ome_cts and elem not in all_ome_attributes:
            print(elem, "   ", tuple[1])

_limi_ome_conv_debugger(limi_elems)

# Debug statements for getting the "Value" elements correctly parsed
# Value needed to be handled separately because it is a nested element only and changes type based on the element within which it is nested
# for elems in all_ome_elements:
#     if "Value" in elems:
#         print(elems, "    ", all_ome_elements[elems].type_)

print("Removed fields debugging: ")
for elems, tuple in limi_elems.items():
    # print(elems, "      ", tuple[0], "  ", tuple[1], "  ", tuple[2])
    if "_rmf" in elems:
        print(elems, "    ", tuple[0])