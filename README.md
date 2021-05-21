# sbol-shacl

This repository contains scripts to generate
[SHACL](https://www.w3.org/TR/shacl/) rules from the SBOL3 ontology
and to validate an SBOL3 file using those SHACL rules.


# Running SHACL generator

The SHACL generator (`shacl_generator.py`) produces SHACL rules from
the SBOL3 ontology file.

By default the SHACL generator will 

```shell
python3 shacl_generator.py rdf/sbol3.ttl -o rdf/sbol3-shapes.ttl
```


# Running the SHACL validator

```shell
python3 shacl_validator.py multicellular.ttl
```
