from limi_ome_converter import *

if __name__ == "__main__":
    limi_data = parse_from_json("../test/ucsd-ren_lab_basct_nikon_eclipse_ti2-u_scope1.json", True)
    convert_to_ome(limi_data)
    