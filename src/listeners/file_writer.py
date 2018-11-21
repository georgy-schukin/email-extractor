class FileWriter(object):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.output = None

    def notify_start(self):
        self.output = open(self.filename, "a")

    def notify_end(self):
        self.output.close()

    def notify_url(self, url):
        pass

    def notify_email(self, email):
        self.output.write(email + "\n")
        self.output.flush()
