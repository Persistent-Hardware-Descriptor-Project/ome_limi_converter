# NBO-to-OME Converter

Python library to convert instances of QUAREP-LiMi 4DN-BINA OME (NBO) microscopy metadata standard to instances of Open Microscopy Environment (OME). 

## Overview

This project aims to convert instances of Quarep-LiMi NBO Microscopy metadata specifications format to instances of Open Microscopy Environment format. The goal is to provide tools for parsing, validating, transforming, and serializing microscopy metadata while maintaining schema compliance. 

## Current Status

This project is under active development.

### Currently Implemented

* Validating QUAREP-LiMi instance against schema 
* Parsing OME schema to Python objects
* Parsing relation between OME schema elements
* Mapping between LiMi and OME schema elements

### Planned

* Converting NBO instances to OME (using mapping and schema definitions)
* Validating OME instances against schema
* Comprehensive testing and error handling


## Getting Started

### Prerequisites
- Python 3.12+
- Required Python libraries (install with `pip install -r requirements.txt`):
  - xmlschema
  - jsonschema
  - ome-types
  - pandas
  - numpy

### Repository Structure

```text
project/
├── src/
│ └── mapping/
├── tests/
├── schemas/
└── README.md
```

### Directories

| Directory      | Description                                             |
| -----------    | ------------------------------------------------------- |
| `src/`         | Source code                                             |
| `src/mapping/` | CSV files with NBO to OME mapping info                  |
| `tests/`       | NBO instance files to test code on                      |
| `schemas/`     | OME and NBO schema definitions (XSD and JSON Schema)    |

## Supported Formats

### Input

* NBO JSON

### Output

* OME XML

## Implementation Notes



## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Open Microscopy Environment (OME)](https://www.openmicroscopy.org/) for the OME schema
- [4DN-BINA-OME (NBO) Microscopy Metadata Specifications](https://github.com/WU-BIMAC/NBOMicroscopyMetadataSpecs/blob/master/Model/stable%20version/v02-01/NBO_MicroscopyMetadataSpecifications_ALL.xsd) for the NBO schemas
- [NBO XLS Worksheet](https://github.com/WU-BIMAC/NBOMicroscopyMetadataSpecs/blob/master/Model/stable%20version/v02-01/NBO_MicroscopyMetadataSpecifications_ALL_v02-01.xlsx) for the NBO to OME mapping and element relationships
