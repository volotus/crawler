#coding:utf-8
#import _env
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gevent.queue import Empty, Queue
import gevent
import gevent.monkey
import requests
from urlparse import urlparse, parse_qs
import re
gevent.monkey.patch_all()


class Bot(object):
    cookie = None
    headers = {}

    def __init__(self, route, timeout=60):
        self.queue = Queue()
        self.timeout = timeout
        self.route = route

    def _fetch(self):
        queue = self.queue
        timeout = self.timeout
        route = self.route
        while True:
            try:
                url = queue.get(timeout=timeout+10)
            except Empty:
                return

            headers = self.headers

            if self.cookie:
                headers['Cookie'] = self.cookie 
            req = requests.get(url, timeout=timeout, headers=headers)
            p = urlparse(req.url)

            cls, args = route.match(p.path)
            if cls:
                o = cls(req)
                r = o.get(*args)
                if r:
                    for i in r:
                        if i:
                            queue.put(i)

    def run(self, num=10):
        for i in xrange(num):
            g = gevent.spawn(self._fetch)
        g.join()

    def put(self, url):
        self.queue.put(url)

class Route(object):
    def __init__(self):
        self.map = []

    def match(self, url):
        for r, f in self.map:
            m = r.match(url)
            if m:
                return f, m.groups()
        return None, None

    def __call__(self, path):
        if not path.endswith('$'):
            path += '$'
        re_path = re.compile(path)
        def _(func):
            self.map.append((re_path, func))
            return func
        return _




from extract import extract, extract_all

class Page(object):

    def __init__(self, req):
        p = urlparse(req.url)
        req.arguments = parse_qs(p.query, 1)
        self.req = req
        self.html = req.content 

    def get_argument(self, name, default=None):
        result = self.req.arguments.get(name, None)
        if result is None:
            return default
        return result[0].encode("utf-8","ignore")
 
    def extract(self, begin, end):
        return extract(begin, end, self.html)
    
    def extract_all(self, begin, end):
        return extract_all(begin, end, self.html)

        



