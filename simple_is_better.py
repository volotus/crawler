#coding:utf-8
#import _env
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from down import Bot , Route, Page
from extract import extract, extract_all
from html2txt import html2txt

route = Route()

@route('/jobs/')
class jobs(Page):
    def get(self):
        page = self.get_argument('page')
        page = int(page)
        if page == 1:
            page_last = self.extract_all('="?page=', '"')[-1]
            for i in xrange(2, int(page_last)+1):
                yield 'http://simple-is-better.com/jobs/?page=%s'%i

        job_list = self.extract_all('<div class="job">', '</div')
        for i in job_list:
            id = extract('"name"><a href="/jobs/', '"', i)
            if not id:
                continue
            yield 'http://simple-is-better.com/jobs/%s'%id


@route('/jobs/(\d+)')
class job(Page):
    def get(self, id):
        name = self.extract('<h1>', '</h1>')

        end = '<div class="box">'
        html = self.extract('<div class="content box">', end)
        html = html[:html.find(end)]
        print '='*50
        print html2txt(name)
        print '='*50
        print html2txt(html)

if __name__ == '__main__':
    #60秒超时
    bot = Bot(route, 60)
    bot.put('http://simple-is-better.com/jobs/?page=1')
    bot.run()



