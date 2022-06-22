from hidateinfer import infer
from datetime import datetime, timezone


class DataTypeConversion:
    def __init__(self):
        self.types = {
            'xsd:dateTime': 'stodt',
            'xsd:int': 'stoi',
            'xsd:boolean': 'stob'
        }

    @staticmethod
    def correct_datatype_format(format: str, hour24: bool = True):
        import re

        if hour24:
            regex = re.compile(r"(^.*T%)(I)(.*)$")
            format = re.sub(regex, r"\1H\3", format)

        regex = re.compile(r"^(.*T%.*:%S\.)(%H)$")
        format = re.sub(regex, r"\1%f", format)

        return format

    def convert(self, data, datatype):
        def stodt(value):
            print(f'toDateTime function, arguments {value}')
            if isinstance(value, str):
                result = infer([value])
            elif isinstance(value, list):
                result = infer(value)
            else:
                raise Exception(f'Invalid format received: {type(value)}')

            result = self.correct_datatype_format(result)

            print(f'format {result}')
            result = datetime.strptime(value, result).replace(tzinfo=timezone.utc).isoformat()
            print(f'result {result}')
            return result

        def stoi(value):
            """
               Converts 'something' to int. Raises exception for invalid formats
            """
            if isinstance(value, str):
                result = value.replace('"', '')
            elif isinstance(value, int):
                result = value
            else:
                raise Exception(f'Invalid format received: {type(value)}')

            return int(result)

        def stob(value):
            """
               Converts 'something' to boolean. Raises exception for invalid formats
                   Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
                   Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
            """
            print(f'toBool function, arguments {value}')

            if str(value).lower() in ("yes", "y", "true", "t", "1"):
                return True

            if str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"):
                return False

            # logger.error(f'Invalid value for boolean conversion: {str(value)}')
            raise Exception(f'Invalid value for boolean conversion: {str(value)}')

        try:
            function = self.types[datatype] + '(value=' + data + ')'
            return eval(function)
        except KeyError:
            # logger.error(f'Datatype not defined: {datatype}')
            print(f'Datatype not defined: {datatype}')
            raise Exception(f'Datatype not defined: {datatype}')
        except NameError:
            # logger.error(f"name '{data}' is not defined")
            print(f"name '{data}' is not defined")
            raise Exception(f"name '{data}' is not defined")


if __name__ == '__main__':
    from lark import Token

    data1 = ['"2022-01-15T08:00:00.000"', Token('FORMATCONNECTOR', '^^'), 'xsd:dateTime']
    data2 = ['"2"', Token('FORMATCONNECTOR', '^^'), 'xsd:int']
    data22 = ['2', Token('FORMATCONNECTOR', '^^'), 'xsd:int']
    data23 = ['asdfs', Token('FORMATCONNECTOR', '^^'), 'xsd:int']
    data3 = ['"true"', Token('FORMATCONNECTOR', '^^'), 'xsd:boolean']
    data4 = ['"fake"', Token('FORMATCONNECTOR', '^^'), 'otraCosa']

    print(infer(['Mon Jan 13 09:52:52 MST 2014']))
    print(infer([data1[0]]))
    print()

    print(infer(['2022-01-15T08:00:00']))
    print(infer([data1[0]]))
    print()

    format = "%Y-%m-%dT%I:%M:%S.%H"
    # Resolve problem in the library
    # if we are working with 24h, infer should return %Y-%m-%dT%H:%M:%S.%f but return %Y-%m-%dT%I:%M:%S.%f
    # if we have seconds with milliseconds, infer should return %Y-%m-%dT%I:%M:%S.%f but return %Y-%m-%dT%I:%M:%S.%H

    dataConversionType = DataTypeConversion()
    print(dataConversionType.convert(data1[0], data1[2]))

    print(dataConversionType.convert(data2[0], data2[2]) + 10)
    print(dataConversionType.convert(data22[0], data22[2]) + 10)
    # print(dataConversionType.convert(data23[0], data23[2]) + 10)

    print(dataConversionType.convert(data3[0], data3[2]))

    print(dataConversionType.convert(data4[0], data4[2]))

    # Convert datetime generated into UTC format: 2021-12-21T16:18:55Z or 2021-12-21T16:18:55+00:00, ISO8601