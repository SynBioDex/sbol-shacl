import argparse
import logging
import os
import posixpath

from pyshacl import validate
from rdflib import Graph


def abs_path(relative_path):  # Expand path based on module installation directory
    return posixpath.join(os.path.dirname(os.path.realpath(__file__)), relative_path)


class ShaclValidator:

    def __init__(self):
        self.g = Graph()
        self.g.parse(abs_path('rdf/sbol3.ttl'), format='ttl')
        # self.g.parse(abs_path('rdf/opil.ttl'), format='ttl')
        # self.g.parse(abs_path('rdf/sd2.ttl'), format='ttl')
        # self.g.parse(abs_path('rdf/om-2.0.rdf'))
        self.g.parse(abs_path('rdf/sbol3-shapes.ttl'), format='ttl')

    def main(self):

        # Load Turtle files into a RDF graph
        print('Loading RDF files...')

        # self.g.parse('rdf/TimeSeriesProtocol.ttl', format='ttl')
        self.g.parse(abs_path('TimeSeriesHTC.ttl'), format='ttl')
        # self.g.parse('rdf/YeastSTATES_1.0_Time_Series_Round_1.ttl', format='ttl')
        # self.g.parse('rdf/TestER.ttl', format='ttl')

        # Do the validation
        print('Validating graph...')
        conforms, results_graph, results_text = \
            validate(self.g, shacl_graph=None, ont_graph=None, inference='rdfs',
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
                        inference='rdfs', abort_on_error=False, meta_shacl=False,
                        advanced=True, debug=False)


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType('r'),
                        metavar="SBOL3_FILE")
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
    validator.main()


if __name__ == '__main__':
    main()
