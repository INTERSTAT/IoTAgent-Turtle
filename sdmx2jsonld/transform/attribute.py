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

from sdmx2jsonld.transform.property import Property


class Attribute(Property):
    def __init__(self):
        super().__init__(entity='AttributeProperty')
        self.data['type'] = 'AttributeProperty'

    def add_data(self, attribute_id, data):
        super().add_data(id=id, data=data)

        # Add the id
        self.data['id'] = "urn:ngsi-ld:AttributeProperty:" + attribute_id
