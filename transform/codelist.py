class CodeList:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "rdfs:Class",
            "rdfs:seeAlso": {
                "type": "Relationship",
                "value": str()
            },
            "rdfs:subClassOf": {
                "type": "Property",
                "value": str()
            },
            "skos:prefLabel": {
                "type": "LanguageProperty",
                "LanguageMap": dict()
            },
            "@context": dict()
        }

    def add_data(self, code_list_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the ConceptSchema: skos:prefLabel
        position = data.index('skos:prefLabel') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            print(f"\nThe CodeList {code_list_id} has a skos:prefLabel without languages: {descriptions}\n\n")

        # Complete the skos:prefLabel
        for i in range(0, len(languages)):
            self.data['skos:prefLabel']['LanguageMap'][languages[i]] = descriptions[i]

        # Add the id
        self.data['id'] = "urn:ngsi-ld:CodeList:" + code_list_id

        # rdfs:seeAlso
        position = data.index('rdfs:seeAlso') + 1
        self.data['rdfs:seeAlso']['value'] = data[position][0]

        # rdfs:subClassOf
        position = data.index('rdfs:subClassOf') + 1
        self.data['rdfs:subClassOf']['value'] = data[position][0]

    def get(self):
        return self.data
