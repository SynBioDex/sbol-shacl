# OWL to SHACL

* https://shacl-play.sparna.fr/play/
  * https://shacl-play.sparna.fr/play/convert
    * Uses https://github.com/sparna-git/owl2shacl for conversion rules
  * https://shacl-play.sparna.fr/play/rules-catalog

Could we execute the conversion rules ourselves? Using pySHACL?

# SBOL3 OWL

See https://github.com/SynBioDex/sbol_factory for the current SBOL3 OWL

# Running

```shell
time python3 shacl_generator.py -o sbol3-shapes.ttl -d
```

Test files:

```shell
for f in $(find /path/to/SBOLTestSuite/SBOL3 -name '*.ttl'); do
  echo $f;
  python3 shacl_validator.py $f;
done
```
