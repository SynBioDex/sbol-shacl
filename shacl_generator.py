import argparse
import logging
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
# Default to canonical SBOL3 Ontology. Users can override the
# ontology on the command line.
SBOL3_OWL = urljoin(GITHUB_RAW,
                    'SynBioDex/sbol-owl3/feature/sbolcomposition/sbolowl3.rdf')


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    # Don't use argparse.FileType('r') because input can be a URL
    # rdflib.Graph.parse automatically handles URLs and filenames
    parser.add_argument('input', nargs='?', metavar='SBOL3_ONTOLOGY',
                        default=SBOL3_OWL)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        default='sbol3-shapes.ttl', metavar='SHACL_RULE_FILE')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%Y-%m-%dT%H:%M:%S%z'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def load_owl(owl_path):
    # Round trip the OWL file through rdflib so that the default prefix
    # gets turned into a labeled prefix, "sbol:".
    owl_graph = rdflib.Graph()
    owl_format = rdflib.util.guess_format(owl_path)
    logging.debug('Loading SBOL3 ontology from %s', owl_path)
    owl_graph.parse(owl_path, format=owl_format)
    tmp_rdf = owl_graph.serialize(format=owl_format)
    owl_graph = rdflib.Graph()
    owl_graph.parse(data=tmp_rdf, format=owl_format)
    return owl_graph


def main(argv=None):
    args = parse_args(argv)
    init_logging(args.debug)

    # Load the owl-to-shacl rules file
    rules_graph = rdflib.Graph()
    logging.debug('Loading owl to shacl rules from %s', OWL2SH)
    rules_graph.parse('owl2sh-sbol-closure.ttl',
                      format=rdflib.util.guess_format('owl2sh-sbol-closure.ttl'))

    # Load the OWL file
    owl_graph = load_owl(args.input)
    logging.debug('Generating SHACL rules')
    result = pyshacl.validate(owl_graph,
                              shacl_graph=rules_graph,
                              ont_graph=None,
                              inference='rdfs',
                              abort_on_first=False,
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
    if args.output.name:
        logging.debug(f'Writing SHACL rules to {args.output.name}')
    else:
        logging.debug('Writing SHACL rules')
    args.output.write(output)
    logging.debug(f'Done.')


if __name__ == '__main__':
    main()
