# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test example app."""

import os
import signal
import subprocess
import sys
import time
import pytest

import pkg_resources

EXAMPLE_APP_DIR = os.path.join(os.path.split(sys.path[0])[0], 'examples')


def setup_module():
    """Set up before all tests."""
    # switch to examples/app.py
    os.chdir(EXAMPLE_APP_DIR)


def teardown_module():
    """Tear down after all tests."""
    for cmd in ['FLASK_APP=app.py flask db destroy --yes-i-know',
                'rm -rf instance']:
        exit_status = subprocess.call(cmd, shell=True)
        assert exit_status == 0


@pytest.mark.skip(reason="no way of currently testing this")
def test_example_app():
    """Test example app."""
    source = pkg_resources.resource_filename('invenio_records',
                                             'data/marc21/bibliographic.xml')
    # Testing database creation
    for cmd in ['mkdir -p instance',
                'pip install -r requirements.txt',
                'FLASK_APP=app.py flask db init',
                'FLASK_APP=app.py flask db create']:
        exit_status = subprocess.call(cmd, shell=True)
        assert exit_status == 0

    # Testing record creation
    cmd = """dojson -i {0} -l marcxml do marc21 | FLASK_APP=app.py \
             flask records create --pid-minter recid""".format(
        source
    )
    exit_status = subprocess.call(cmd, shell=True)
    assert exit_status == 0

    # Download javascript and css libraries
    for cmd in ['FLASK_APP=app.py flask npm',
                'cd static && npm install && cd ..',
                'npm install -g node-sass@3.8.0 clean-css@3.4.12'
                ' requirejs uglify-js',
                'FLASK_APP=app.py flask collect -v',
                'FLASK_APP=app.py flask assets build']:
        exit_status = subprocess.call(cmd, shell=True)
        assert exit_status == 0

    # Starting example web app
    cmd = 'FLASK_APP=app.py flask run'
    webapp = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              preexec_fn=os.setsid, shell=True)
    time.sleep(10)

    # Testing record retrieval via web
    cmd = 'curl http://127.0.0.1:5000/example/1'
    output = subprocess.check_output(cmd, shell=True)
    assert 'Candidate of Higgs boson production' in str(output)

    # Stopping example web app
    os.killpg(webapp.pid, signal.SIGTERM)
