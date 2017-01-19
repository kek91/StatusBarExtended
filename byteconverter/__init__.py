# Utility class for converting bytes

class ByteConverter():
    def __init__(self, n):
        self.bytes = n
    def calc(self):
        for x in ['B', 'KB', 'MB', 'GB', 'TB']:
            if self.bytes < 1024.0:
                return "%3.1f %s" % (self.bytes, x)
            self.bytes /= 1024.0
