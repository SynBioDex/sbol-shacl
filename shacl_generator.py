import argparse
import logging
import sys
from urllib.parse import urljoin

import pyshacl
import rdflib

GITHUB_RAW = 'https://raw.githubusercontent.com/'

# We use the semi-closed version of owl2sh. owl2sh-open and
# owl2sh-closed do not work well for SBOL3.
OWL2SH = urljoin(GITHUB_RAW,
                 '/sparna-git/owl2shacl/main/owl2sh-semi-closed.ttl')

# SBOL 3 Ontology
# ---------------
# Default to the version stored at Goksel Misirli's GitHub. This should
# eventually move to a more official area, perhaps in the SynBioDex
# organization. Update this location if it is moved to a canonical
# location.
SBOL3_OWL = urljoin(GITHUB_RAW, 'dissys/sbol-owl3/main/sbolowl3.rdf')


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    # Don't use argparse.FileType('r') because input can be a URL
    # rdflib.Graph.parse automatically handles URLs and filenames
    parser.add_argument('input', metavar='SBOL3_ONTOLOGY',
                        default=SBOL3_OWL)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        default=sys.stdout, metavar='SHACL_RULE_FILE')
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

    # Load the owl-to-shacl rules file
    rules_graph = rdflib.Graph()
    logging.debug('Loading owl to shacl rules from %s', OWL2SH)
    rules_graph.parse(OWL2SH,
                      format=rdflib.util.guess_format(OWL2SH))

    # Load the OWL file
    owl_graph = rdflib.Graph()
    owl_format = rdflib.util.guess_format(args.input)
    logging.debug('Loading SBOL3 ontology from %s', args.input)
    owl_graph.parse(args.input, format=owl_format)

    result = pyshacl.validate(owl_graph,
                              shacl_graph=rules_graph,
                              ont_graph=None,
                              inference='rdfs',
                              abort_on_error=False,
                              meta_shacl=False,
                              advanced=True,
                              debug=True,
                              inplace=True)
    # Unpack pyshacl.validate's return tuple
    conforms, results_graph, results_text = result
    if not conforms:
        logging.error('Unable to generate shacl rules.')
        logging.error(results_text)
        return
    owl_graph.namespace_manager.bind('dash', 'http://datashapes.org/dash#')
    owl_graph.namespace_manager.bind('sh', 'http://www.w3.org/ns/shacl#')
    output = owl_graph.serialize(format='ttl')
    args.output.write(output.decode('utf8'))


if __name__ == '__main__':
    main()
