# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Permanent redirects to support the website re-organization and merging of
browser.datacommons.org with datacommons.org
"""

import json

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import request
from flask import url_for

from server.lib.config import GLOBAL_CONFIG_BUCKET
from shared.lib import gcs

bp = Blueprint(
    "redirects",
    __name__,
)


@bp.route('/kg')
def kg():
  dcid = request.args.get('dcid', '')
  if dcid:
    url = url_for('browser.browser_node', dcid=dcid)
  else:
    url = url_for('browser.browser_main')
  return redirect('https://datacommons.org' + url, code=302)


@bp.route('/gni')
def gni():
  return redirect(
      url_for('tools.timeline',
              _external=True,
              _scheme=current_app.config.get('SCHEME', 'https'),
              code=302))


@bp.route('/scatter')
def scatter():
  return redirect(
      url_for('tools.scatter',
              _external=True,
              _scheme=current_app.config.get('SCHEME', 'https'),
              code=302))


# Note: The trailing '/' helps in redirecting `/nlnext/#q=some+query+here` to `/nl/#q=some+query+here`
@bp.route('/nlnext/')
@bp.route('/nlnext')
def nlnext():
  return redirect(url_for('explore.page'), code=302)


@bp.route('/datasets')
def datasets():
  return redirect(url_for('static.data'), code=301)


@bp.route('/documentation')
def documentation():
  return redirect('https://docs.datacommons.org/', code=302)


@bp.route('/colab')
def colab():
  return redirect('https://docs.datacommons.org/tutorials', code=302)


@bp.route('/getinvolved')
def get_involved():
  return redirect('https://docs.datacommons.org/contributing/', code=302)


@bp.route('/tools/stat-var')
def stat_var():
  return redirect('https://datacommons.org/tools/statvar', code=302)


@bp.route('/insights/')
def insights():
  return redirect(
      url_for('explore.page',
              _scheme=current_app.config.get('SCHEME', 'https'),
              code=302))


@bp.route('/demo')
def demo():
  return redirect('/link/demo', code=302)


@bp.route('/link/<path:name>')
def link(name):
  redirection_mapping = current_app.config.get('REDIRECTS', {})
  return redirect(redirection_mapping.get(name, '/'), code=302)
