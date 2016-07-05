import newspaper

class News(object):
    def get_hot(self):
        return newspaper.hot()