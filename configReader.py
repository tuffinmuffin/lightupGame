# -*- coding: utf-8 -*-

import logging
log = logging.getLogger()

import configparser


class Configuration:
    
    #init code. takes config file.
    def __init__(self, configFile):
        self.colors = {}
        self.apa102 = {}
        self.patterns = {}
        self.network = {}
        self.app = {}
        
        config = configparser.ConfigParser()
        config.read(configFile)
        self.config = config
        
        self.parseColors()
        self.parseApa102()
        self.parseNetwork()
        self.parseApp()
        self.parsePatterns()
        
        
    def parseColors(self):
        colors = {}
        self.parseGeneric("COLORS", colors)
        for key in colors:
            try:
                self.colors[key] = int(self.config['COLORS'][key].lstrip().lstrip("#"),16)
            except:
               # print(log)
                log.warning("Failed to parse color %s:%s"%(key,self.config['COLORS'][key]))

        return self.colors
    
    def parseApa102(self):
        return self.parseGeneric("APA102",self.apa102)
    
    def parseNetwork(self):
        return self.parseGeneric("NETWORK", self.network)
    
    def parseApp(self):
        return self.parseGeneric("APP", self.app)

    def parsePatterns(self):
        return self.parseGeneric("PATTERNS", self.patterns)

    def parseGeneric(self, field, output):
        if not field in self.config.sections():
            log.warning("No %s config found"%(field))
            return output
        for key in self.config[field]:
            output[key] = self.config[field][key]
        print(output)
        return output
    


if __name__ == "__main__":
    file = "sampleConfig.ini"
    
    config = Configuration(file)
    
    
    