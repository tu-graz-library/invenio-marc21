# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
# Copyright (C) 2020 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Nice defaults for an overlay using MARC21 format."""

import copy

from invenio_records_rest.config import RECORDS_REST_ENDPOINTS
from invenio_records_rest.query import es_search_factory
from invenio_records_rest.utils import allow_all, check_elasticsearch
from invenio_records_ui.config import RECORDS_UI_ENDPOINTS
from invenio_search import RecordsSearch

MARC21_REST_ENDPOINTS = {
    "recid": dict(
        pid_type="recid",
        pid_minter="recid",
        pid_fetcher="recid",
        default_endpoint_prefix=True,
        record_class="invenio_records.api:Record",
        search_class=RecordsSearch,
        search_index=None,
        search_type=None,
        record_serializers={
            "application/json": "invenio_records_rest.serializers:json_v1_response",
            "application/marcxml+xml": (
                "invenio_marc21.serializers:marcxml_v1_response"
            ),
            "application/mods+xml": "invenio_marc21.serializers:mods_v1_response",
            "application/xml": "invenio_marc21.serializers:dublincore_v1_response",
        },
        search_serializers={
            "application/json": "invenio_records_rest.serializers:json_v1_search",
            "application/marcxml+xml": ("invenio_marc21.serializers:marcxml_v1_search"),
            "application/mods+xml": "invenio_marc21.serializers:mods_v1_search",
            "application/xml": "invenio_marc21.serializers:dublincore_v1_search",
        },
        # TODO: create my own loader for application/marcxml+xml
        # record_loaders={
        #    "application/json": ("invenio_marc21.loaders" ":json_v1"),
        # },
        list_route="/marc/",
        item_route="/marc/<pid(recid):pid_value>",
        default_media_type="application/json",
        max_result_window=10000,
        error_handlers=dict(),
        create_permission_factory_imp=allow_all,
        read_permission_factory_imp=check_elasticsearch,
        update_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
    ),
}


# TODO: implement ui endpoints
# MARC21_UI_EXPORT_FORMATS = {
#    "recid": {
#        "marcxml": dict(
#            title="MARCXML",
#            serializer="invenio_marc21.serializers.marcxml_v1",
#            order=1,
#        ),
#        "mods": dict(
#            title="MODS",
#            serializer="invenio_marc21.serializers.mods_v1",
#            order=2,
#        ),
#        "dc": dict(
#            title="DublinCore",
#            serializer="invenio_marc21.serializers.dublincore_v1",
#            order=3,
#        ),
#        "json": dict(
#            title="JSON",
#            serializer="invenio_records_rest.serializers.json_v1",
#            order=4,
#        ),
#       # Deprecated names
#        "hx": False,
#        "hm": False,
#        "xm": False,
#        "xd": False,
#        "xe": False,
#        "xn": False,
#        "xw": False,
#    }
# }

# MARC21_UI_ENDPOINTS = copy.deepcopy(RECORDS_UI_ENDPOINTS)
# MARC21_UI_ENDPOINTS['recid']['template'] = 'invenio_marc21/detail.html'
# MARC21_UI_ENDPOINTS['recid_export'] = {
#    'pid_type': 'recid',
#    'route': '/record/<pid_value>/export/<any({0}):format>'.format(
#        ', '.join(list(MARC21_UI_EXPORT_FORMATS['recid'].keys()))),
#    'template': 'invenio_marc21/export.html',
#    'view_imp': 'invenio_records_ui.views.export',
