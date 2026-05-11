class Data:
    def __init__(self, data):
        data = data.decode("UTF-8")
        self.endpoint, self.payload = data.split(";")

    def is_empty(self):
        return len(self.endpoint) == 0 and len(self.payload) == 0

    def full_data(self):
        return ";".join([self.endpoint, self.payload]).encode()
