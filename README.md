# sbol-shacl

This repository contains scripts to generate
[SHACL](https://www.w3.org/TR/shacl/) rules from the SBOL3 ontology
and to validate an SBOL3 file using those SHACL rules.


# Running the SHACL generator

The SHACL generator (`shacl_generator.py`) produces SHACL rules from
the SBOL3 ontology file.

By default the SHACL generator will use the canonical SBOL3 OWL file
at https://github.com/SynBioDex/sbol-owl3, and write the generated
SHACL rules to standard out. The output path can be overridden using
the `-o` command line option as shown below.

```shell
python3 shacl_generator.py -o rdf/sbol3-shapes.ttl
```

Run with the `-h` command line option to see the full set of
command line arguments.

```shell
python3 shacl_generator.py -h
```


# Running the SHACL validator

The SHACL validator (`shacl_generator.py`) will validate an SBOL3 file
using the SHACL rules in `rdf/sbol3-shapes.ttl`.

```shell
python3 shacl_validator.py SBOL_FILE
```
