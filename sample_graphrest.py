"""graphrest sample for Microsoft Graph"""
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.

import bottle
import graphrest
import requests

import config

MSGRAPH = graphrest.GraphSession(client_id=config.CLIENT_ID,
                                 client_secret=config.CLIENT_SECRET,
                                 redirect_uri=config.REDIRECT_URI,
                                 scopes=['User.Read'])

bottle.TEMPLATE_PATH = ['./static/templates']

@bottle.route('/')
@bottle.view('homepage.html')
def homepage():
    """Render the home page."""

    return {'sample': 'graphrest'}

@bottle.route('/login')
def login():
    """Prompt user to authenticate."""
    MSGRAPH.login()

@bottle.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""
    MSGRAPH.redirect_uri_handler(redirect_to='/graphcall')

@bottle.route('/graphcall')
@bottle.view('graphcall.html')
def graphcall():
    """Confirm user authentication by calling Graph and displaying some data."""
    MSGRAPH.token_validation() # Optional - assures token is valid for >5 seconds.
    endpoint = MSGRAPH.api_endpoint('me')
    graphdata = requests.get(endpoint, headers=MSGRAPH.headers()).json()
    return {'graphdata': graphdata,
            'endpoint': MSGRAPH.api_endpoint(endpoint),
            'sample': 'graphrest'}

if __name__ == '__main__':
    bottle.run(app=bottle.app(), server='wsgiref', host='localhost', port=5000)
