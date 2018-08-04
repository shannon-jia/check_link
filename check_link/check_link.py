# -*- coding: utf-8 -*-

"""Main module."""

import logging
import asyncio
import json
import aiohttp
from itertools import groupby

log = logging.getLogger(__name__)


class CheckLink:
    def __init__(self, loop, url, db):
        self.loop = loop or asyncio.get_event_loop()
        self.db = db
        self.url = url

        self.device_data = {}
        self.spk_link = []
        self.cam_link = []
        self.lost = []

    async def get(self, session):
        async with session.get(self.url) as response:
            return await response.text()

    async def fetch(self):
        try:
            async with aiohttp.ClientSession() as session:
                result = await self.get(session)
                mesg = json.loads(result)
                if not mesg.get('system'):
                    log.warning('Please check the svc_uri: {}'.format(self.url))
                    return
                self.device_data = mesg
        except Exception as e:
            log.error(e)

    def preset_device(self):
        asyncio.ensure_future(self.fetch())

    def preset_link(self):
        asyncio.ensure_future(self.get_links())

    def start(self):
        self._auto_loop()

    def _auto_loop(self):
        self.lost = []
        self.preset_device()
        self.preset_link()
        self.do_computation(self.spk_link)
        self.do_computation(self.cam_link)
        self.loop.call_later(10, self._auto_loop)

    async def find(self, collection, conditions=None):
        result = []
        try:
            result = await self.db.do_find(collection, conditions)
        except Exception as e:
            log.error('Connect to database has Error: {}'.format(e))
        return result

    async def get_links(self):
        self.spk_link = []
        self.cam_link = []
        links_list = await self.find('links')
        links = links_list
        for link in links:
            if 'SPK' in link.get('action', ''):
                self.spk_link.append(link)
            elif 'CAM' in link.get('action', ''):
                self.cam_link.append(link)
            else:
                pass

    def grep_device_data(self):
        segs_info = []
        if not self.device_data:
            return
        for line in self.device_data.get('system'):
            sys_num = int(line.get('line', 0))
            segments = line.get('display_segments', '')
            if not segments:
                return
            for seg in segments:
                _seg = {}
                if seg.get('unit', 0) == 0:
                    continue
                _seg['name'] = 'SEG_' + str(sys_num) + '_' + str(seg.get('seg_no', 0))
                _seg['start'] = int(seg.get('start', 0))
                _seg['end'] = int(seg.get('end', 0))
                segs_info.append(_seg)
        return segs_info

    def do_computation(self, which_link):
        if which_link == self.spk_link:
            event = 'SPK'
        elif which_link == self.cam_link:
            event = 'CAM'
        else:
            event = None
        segs_info = self.grep_device_data()
        if not segs_info or not which_link:
            return
        for seg in segs_info:
            _miss = {}
            seg_set = set()
            link_set = set()
            _s = int(seg.get('start', 0))
            _e = int(seg.get('end', 0))
            seg_set.update(range(min(_s, _e), max(_s, _e)+1))
            for i in which_link:
                if seg.get('name', '') == i.get('name', ''):
                    link_set.update(range(int(i.get('min', 0)),
                                          int(i.get('max', 0)+1)))
            same = seg_set.intersection(link_set)
            diff = seg_set.difference(same)
            if diff:
                _miss['name'] = seg.get('name', '')
                _miss['event'] = event
                _miss['miss_point'] = self._get_scope(diff)
                self.lost.append(_miss)
                log.warning('Unlinked point is {}'.format(_miss))
        if not self.lost:
            log.info('All point be linked!')

    def _get_scope(self, points):
        scope_lst = []
        _lst = [j for j in points]
        for i in range(len(_lst)):
            j = i+1
            for j in range(len(_lst)):
                if _lst[i] < _lst[j]:
                    x = _lst[i]
                    _lst[i] = _lst[j]
                    _lst[j] = x
        fun = lambda x: x[0]-x[1]
        for k, g in groupby(enumerate(_lst), fun):
            l1 = [j for i, j in g]
            if len(l1) > 1:
                s = str(min(l1)) + '-' + str(max(l1))
            else:
                s = str(l1[0])
            scope_lst.append(s)
        return scope_lst

    def get_info(self):
        with open("miss_point.json", "w") as f:
            json.dump(self.lost, f)
        return {'unlink_point': self.lost}
