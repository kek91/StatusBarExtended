# Utility class for converting bytes

import statusbarextended_config as SBEcfg

class ByteConverter():
    def __init__(self, n):
        self.bytes = n
        cfg = SBEcfg.SingletonConfig()
        cfgCurrent, exit_status = cfg.loadConfig()
        if cfgCurrent is None:
            self.sizeDivisor = cfg.Default['SizeDivisor']
        else:
            self.sizeDivisor =  cfgCurrent['SizeDivisor']
    def calc(self):
        for x in ['b', 'k', 'M', 'G', 'T']:
            if self.bytes < self.sizeDivisor:
                return "%3.1f %s" % (self.bytes, x) if x!='b' else "%5.0f" % (self.bytes)
            self.bytes   /= self.sizeDivisor
