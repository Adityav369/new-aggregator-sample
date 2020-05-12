import datetime
class News(object):
    def __init__(self, title, day, detail, company, link):
        self.title = title
        self.day = day
        self.detail = detail
        self.company = company
        self.link = link
