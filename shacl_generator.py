import argparse
import logging
import sys

import pyshacl
import rdflib

# OWL2SH = 'https://raw.githubusercontent.com/sparna-git/owl2shacl/main/owl2sh-open.ttl'
OWL2SH = 'https://raw.githubusercontent.com/sparna-git/owl2shacl/main/owl2sh-semi-closed.ttl'

# Closed has 2 problems:
#   * It doesn't generate properly - it lacks in rdf namespace declaration and I don't know why
#   * It generates lots of errors on our files which we probably don't want.
# OWL2SH = 'https://raw.githubusercontent.com/sparna-git/owl2shacl/main/owl2sh-closed.ttl'
SBOL3_OWL = 'https://raw.githubusercontent.com/SynBioDex/sbol_factory/master/sbol_factory/rdf/sbol3.ttl'
SBOL3_OWL = 'rdf/sbol3.ttl'

def parse_args(args=None):
    parser = argparse.ArgumentParser()
    # parser.add_argument("infile", metavar="SBOL3_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        default=sys.stdout)
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def main(argv=None):
    args = parse_args(argv)
    init_logging(args.debug)

    # Load the owl-to-shacle rules file
    rules_graph = rdflib.Graph()
    rules_graph.parse(OWL2SH,
                      format=rdflib.util.guess_format(OWL2SH))

    # Load the OWL file
    owl_graph = rdflib.Graph()
    owl_graph.parse(SBOL3_OWL,
                    format=rdflib.util.guess_format(SBOL3_OWL))

    # data_graph = rdflib.Graph()
    # data_graph += owl_graph

    r = pyshacl.validate(owl_graph,
                         shacl_graph=rules_graph,
                         ont_graph=None,
                         # inference='rdfs',
                         abort_on_error=False,
                         meta_shacl=False,
                         advanced=True,
                         debug=True,
                         inplace=True)
    # TODO: Check results here
    # data_graph -= owl_graph
    # for prefix, namespace in rules_graph.namespaces():
    #     logging.debug(f'Binding {prefix} to {namespace}')
    #     data_graph.namespace_manager.bind(prefix, namespace)
    owl_graph.namespace_manager.bind('dash', 'http://datashapes.org/dash#')
    owl_graph.namespace_manager.bind('sh', 'http://www.w3.org/ns/shacl#')
    # data_graph.namespace_manager.bind('rdf', str(rdflib.RDF))
    output = owl_graph.serialize(format='ttl')
    # args.output.write('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .')
    # args.output.write(os.linesep)
    args.output.write(output.decode('utf8'))


if __name__ == '__main__':
    main()
