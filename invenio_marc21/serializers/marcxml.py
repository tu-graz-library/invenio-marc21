# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""MARC21 based serializer."""

from __future__ import absolute_import, print_function

from dojson.contrib.to_marc21.utils import dumps, dumps_etree
from invenio_records.api import Record

from .dojson import DoJSONSerializer


class MARCXMLSerializer(DoJSONSerializer):
    """DoJSON based MARCXML serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records due to high memory usage.
    """

    def __init__(self, dojson_model, xslt_filename=None, schema_class=None,
                 replace_refs=False):
        """Initialize serializer.

        :param dojson_model: The DoJSON model able to convert JSON through the
            ``do()`` function.
        :param xslt_filename: XSLT filename. (Default: ``None``)
        :param schema_class: The schema class. (Default: ``None``)
        :param replace_refs: Boolean value to configure if replace the ``$ref``
            keys within the JSON. (Default: ``False``)
        """
        self.dumps_kwargs = dict(xslt_filename=xslt_filename) if \
            xslt_filename else {}

        self.schema_class = schema_class
        super(MARCXMLSerializer, self).__init__(
            dojson_model, replace_refs=replace_refs)

    def dump(self, obj):
        """Serialize object with schema.

        :param obj: The object to serialize.
        :returns: The object serialized.
        """
        if self.schema_class:
            obj = dict(self.schema_class().dump(obj).items())
        else:
            obj = obj['metadata']
        return super(MARCXMLSerializer, self).dump(obj)

    def serialize(self, pid, record, links_factory=None):
        """Serialize a single record and persistent identifier.

        :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
            instance.
        :param record: The :class:`invenio_records.api.Record` instance.
        :param links_factory: Factory function for the link generation,
            which are added to the response.
        :returns: The object serialized.
        """
        return dumps(self.transform_record(pid, record, links_factory),
                     **self.dumps_kwargs)

    def serialize_search(self, pid_fetcher, search_result,
                         item_links_factory=None, **kwargs):
        """Serialize a search result.

        :param pid_fetcher: Persistent identifier fetcher.
        :param search_result: Elasticsearch search result.
        :param item_links_factory: Factory function for the items in result.
            (Default: ``None``)
        :returns: The objects serialized.
        """
        ret = [self.transform_search_hit(pid_fetcher(hit['_id'],
                                         hit['_source']),
                                         hit,
                                         links_factory=item_links_factory)
               for hit in search_result['hits']['hits']]

        return dumps(ret, **self.dumps_kwargs)

    def serialize_oaipmh(self, pid, record):
        """Serialize a single record for OAI-PMH.

        :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
            instance.
        :param record: The :class:`invenio_records.api.Record` instance.
        :returns: The object serialized.
        """
        obj = self.transform_record(pid, record['_source']) \
            if isinstance(record['_source'], Record) \
            else self.transform_search_hit(pid, record)

        return dumps_etree(obj, **self.dumps_kwargs)
