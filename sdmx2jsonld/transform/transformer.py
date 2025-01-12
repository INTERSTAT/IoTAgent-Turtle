#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2022 FIWARE Foundation, e.V.
#
# This file is part of IoTAgent-SDMX (RDF Turtle)
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

from lark import Transformer, Tree, Token
from sdmx2jsonld.transform.context import Context
from sdmx2jsonld.transform.entitytype import EntityType
from sdmx2jsonld.common.datatypeconversion import DataTypeConversion
import re


class TreeToJson(Transformer):
    def __init__(self):
        super().__init__()
        self.context = Context()
        self.entity_type = EntityType()

        # Regex to check valid URL
        # regex = "<http[s]?:\/\/(.*)>"
        regex = "http[s]?:\/\/(.*)"

        # Compile the Regex
        self.re = re.compile(regex)

    def prefixid(self, s):
        context = dict()
        context[str(s[0].children[0])] = s[1]
        self.context.add_context(context)

    def triples(self, triple):
        self.entity_type.set_context(context=self.get_context(), mapping=self.get_context_mapping())
        self.entity_type.transform(string=triple)
        return triple

    def predicate(self, pre):
        result = ''
        if isinstance(pre[0], str):
            result = pre[0]
        else:
            result = str(pre[0].children[0].children[0])

        return result

    def subject(self, sub):
        return sub[0]

    def predicateobjectlist(self, pol):
        return pol

    def objectlist(self, ol):
        return ol

    def prefixedname(self, pre):
        return str(pre[0])

    def string(self, a):
        return str(a[0])

    def rdfliteral(self, a):
        return a

    def rdfliteralformat(self, connector):
        data_conversion_type = DataTypeConversion()
        data = data_conversion_type.convert(connector[0], connector[2])

        return data

    def langtag(self, tag):
        return str(tag[0])

    def iri(self, iri):
        return str(iri[0])
        # return iri

    def verb(self, verb):
        return str(verb[0])

    def object(self, object):
        return object[0]

    def literal(self, literal):
        return literal[0]

    def uriref(self, uriref):
        return str(uriref[0])

    def blanknodepropertylist(self, property_list):
        self.entity_type.transform(string=property_list)
        return property_list

    def get_context(self):
        return self.context.get_context()

    def get_context_mapping(self):
        return self.context.get_context_mapping()

    def get_catalogue(self):
        return self.entity_type.get_catalogue()

    def get_dataset(self):
        return self.entity_type.get_dataset()

    def get_dimensions(self):
        return self.entity_type.get_dimensions()

    def get_attributes(self):
        return self.entity_type.get_attributes()

    def get_conceptSchemas(self):
        return self.entity_type.get_conceptSchemas()

    def get_conceptLists(self):
        return self.entity_type.get_conceptList()

    def save(self):
        self.entity_type.save('catalogue')

        self.entity_type.save('dataset')

        dimensions = self.entity_type.get_dimensions()
        [dimension.save() for dimension in dimensions]

        attributes = self.entity_type.get_attributes()
        [attribute.save() for attribute in attributes]

        concept_schemas = self.entity_type.get_conceptSchemas()
        [x.save() for x in concept_schemas]

        concept_lists = self.entity_type.get_conceptList()
        [x.save() for x in concept_lists]

