# Utility class for converting bytes

class ByteConverter():
    def __init__(self, n):
        self.bytes = n
    def calc(self):
        for x in ['b', 'k', 'M', 'G', 'T']:
            if self.bytes < 1024.0:
                return "%3.1f %s" % (self.bytes, x) if x!='b' else "%5.0f" % (self.bytes)
            self.bytes /= 1024.0
