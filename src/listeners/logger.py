class Logger(object):
    def __init__(self):
        super().__init__()

    def notify_start(self):
        pass

    def notify_end(self):
        pass

    def notify_url(self, url):
        print("URL: " + url)

    def notify_email(self, email):
        print("Email: " + email)
