import argparse
import logging
import os

from pyshacl import validate
import rdflib


def abs_path(relative_path):
    """Expand the given path based on the module installation
    directory.
    """
    module_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(module_path, relative_path)


class ShaclValidator:

    def __init__(self):
        self.g = rdflib.Graph()
        # self.g.parse(abs_path('rdf/sbol3.ttl'), format='ttl')
        shacl_path = os.path.join('rdf', 'sbol3-shapes.ttl')
        rdf_format = rdflib.util.guess_format(shacl_path)
        self.g.parse(abs_path(shacl_path), format=rdf_format)

    def main(self, infile):

        # Load Turtle files into a RDF graph
        print('Loading RDF files...')

        # self.g.parse('rdf/TimeSeriesProtocol.ttl', format='ttl')
        rdf_format = rdflib.util.guess_format(infile)
        self.g.parse(infile, format=rdf_format)

        # Do the validation
        logging.debug('Running validation rules')
        conforms, results_graph, results_text = \
            validate(self.g, shacl_graph=None, ont_graph=None,
                     # inference='rdfs',
                     abort_on_error=False, meta_shacl=False,
                     advanced=True, debug=False)

        if conforms:
            print('Graph is valid')
        else:
            print('Graph is invalid:\n')
            print(results_text)

        # Query the results graph to find the problem instances
        # bad_things_query = self.load_sparql('sparql/badInstances.sparql')
        # query_results = results_graph.query(bad_things_query)

        # if query_results:
        # for row in query_results:
        #     print('{}: {}'.format(row.msg.value, row.bad))

    def load_sparql(self, file_path):
        with open(file_path, 'r') as query_file:
            # Strip newline characters and concatenate lines
            query = ' '.join([line.strip() for line in query_file])
        return query

    def validate(self, graph_to_validate):
        g = graph_to_validate + self.g
        return validate(g, shacl_graph=None, ont_graph=None,
                        inference='rdfs', abort_on_error=False,
                        meta_shacl=False, advanced=True, debug=False)


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", metavar="SBOL3_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
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

    validator = ShaclValidator()
    validator.main(args.infile)


if __name__ == '__main__':
    main()
