#coding:utf-8
from down import Bot , Route, Page
from extract import extract, extract_all
from html2txt import html2txt

route = Route()

@route('/index')
class renren(Page):
    def get(self):
        print self.html

if __name__ == '__main__':
    #60秒超时
    bot = Bot(route, 60)
    bot.cookie =  "__utma=264742537.1644416817.1342959642.1342959642.1343108888.2; __utmz=264742537.1342959642.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); uid=AaKcHFCFV58qdGJ%2B1RKnVQQMy8no9fBilqfbgLFPCO4wn5xeS9fboXHbMhG77tm1BQ%3D%3D; JSESSIONID=2D9F7264AED01BFD15A6ED52C780668E-c1.web-6; __utmb=264742537.1.10.1343108888; __utmc=264742537"
    bot.put('http://www.wumii.com/index')
    bot.run()




