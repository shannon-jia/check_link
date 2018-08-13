#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The Application Interface."""

import logging
import asyncio
import json
from aiohttp import web

log = logging.getLogger(__name__)


class Api(object):
    ''' Application Interface for RPS
    '''

    def __init__(self, loop, port=8080, site=None):
        loop = loop or asyncio.get_event_loop()
        self.app = web.Application(loop=loop)
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/v2/miss_link', self.handle_mlink)
        self.app.router.add_get('/v2/miss_seg', self.handle_mseg)
        self.site = site
        self.port = port
        self.db = {}

    def start(self):
        # outside
        web.run_app(self.app, host='0.0.0.0', port=self.port)

    async def index(self, request):
        return web.Response(text=json.dumps({
            'info': str(self.site),
            'name': 'Linker for IPP-ONE',
            'api_version': 'V1',
            'MLink_api': ['v2/miss_link'],
            'MSeg_api': ['v2/miss_seg'],
            'modules version': 'IPP-I'}))

    async def handle_mlink(self, request):
        data = self.site.get_mlink()
        return web.Response(
            text=json.dumps(data))

    async def handle_mseg(self, request):
        data = self.site.get_mseg()
        return web.Response(
            text=json.dumps(data))
