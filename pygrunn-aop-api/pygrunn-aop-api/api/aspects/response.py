import json
from lxml import etree
from django.http import HttpResponse


def xml_write_value(val):
    """
    Create an XML tree containing values the client requests.

    Parameters:
    - val       list(dict(String,var))  A list containing dictionaries with the values to return

    Return:
    HttpResponse object containing values the client requests in XML as a body with the mimetype 'application/xml'.
    """
    result = etree.Element('result')
    result.text = str(val).decode('utf-8')

    response = HttpResponse(etree.tostring(result), 'application/xml')
    response['Cache-Control'] = 'no-cache'
    return response


def json_write_value(val):
    """
    Create a JSON representation of the values the client requests.

    Parameters:
    - val       list/dict   A list or a dictionary that will be converted to a JSON representation

    Return:
    HttpResponse object containing values the client requests in a JSON representation with the mimetype
    'application/json'.
    """
    response = HttpResponse(json.dumps(val), 'application/json')
    response['Cache-Control'] = 'no-cache'
    return response


def response(function):
    def advice(request, format, *args, **kwargs):
        if not format in ['html', 'xml', 'json']:
            # raise an error if the format specified is not supported
            raise Exception('The format "{0}" is not supported'.format(format))

        ret = function(request, *args, **kwargs)

        # post-process the result of the function to be decorated by formatting the response
        if format == 'html':
            return HttpResponse(ret)
        elif format == 'xml':
            return xml_write_value(ret)
        elif format == 'json':
            return json_write_value(ret)
    return advice
