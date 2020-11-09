# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
# Copyright (C) 2020 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

docker-services-cli up postgresql es redis && \
pydocstyle invenio_marc21 tests docs && \
check-manifest --ignore ".travis-*" && \
python -m sphinx.cmd.build -qnNW docs docs/_build/html && \
docker-services-cli up es postgresql redis
python -m pytest
tests_exit_code=$?
docker-services-cli down
exit "$tests_exit_code" 