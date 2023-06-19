from unittest import TestCase
from sdmx2jsonld.common.rdf import turtle_terse
from rdflib import Graph

class TestRegToParser(TestCase):
    def setUp(self) -> None:
        pass

    def test_turtle_1(self):
        rdf_data = '''
@prefix ab: <http://learningsparql.com/ns/addressbook#> .

ab:richard ab:homeTel "(229) 276-5135" .
ab:richard ab:email   "richard49@hotmail.com" .

ab:cindy ab:homeTel "(245) 646-5488" .
ab:cindy ab:email   "cindym@gmail.com" .

ab:craig ab:homeTel "(194) 966-1505" .
ab:craig ab:email   "craigellis@yahoo.com" .
ab:craig ab:email   "c.ellis@usairwaysgroup.com" .
        '''
        rdf_content = turtle_terse(rdf_data)
        
        gx = Graph()
        gx = gx.parse(data=rdf_content, format="turtle")
        ser = gx.serialize(format="turtle")

        assert(rdf_content == ser)
