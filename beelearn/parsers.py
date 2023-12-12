import json
from django.conf import settings
from django.http.multipartparser import MultiPartParser
from django.http.multipartparser import MultiPartParserError

from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser, DataAndFiles


def loads(input):
    if isinstance(input, list):
        for index, item in enumerate(input):
            input[index] = loads(item)
    elif isinstance(input, str):
        return json.loads(input)

    return input


class JSONMultipartParser(BaseParser):
    """
    Parser for multipart form data, which may include file data.
    """

    media_type = "multipart/form-data"

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as a multipart encoded form,
        and returns a DataAndFiles object.

        `.data` will be a `QueryDict` containing all the form parameters.
        `.files` will be a `QueryDict` containing all the form files.
        """
        parser_context = parser_context or {}
        request = parser_context["request"]
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta["CONTENT_TYPE"] = media_type
        upload_handlers = request.upload_handlers

        try:
            parser = MultiPartParser(meta, stream, upload_handlers, encoding)
            data, files = parser.parse()

            return DataAndFiles(data, files)
        except MultiPartParserError as exc:
            raise ParseError("Multipart form parse error - %s" % str(exc))
