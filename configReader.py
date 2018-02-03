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
        config.optionxform = str 
        config.read(configFile)
        self.config = config
        
        self.parseColors()
        self.parseApa102()
        self.parseNetwork()
        self.parseApp()
        self.parsePatterns()
        
    
    def getValue(self, data, name, default):
        try:
            return data[name]
        except:
            log.warning("No config found for %s using %s"%(name,default))
            return default
        
        
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
        self.parseGeneric("APA102",self.apa102)
        
        for key in self.apa102:
            try:
                self.apa102[key] = int(self.apa102[key])
            except:
                pass    
        return self.apa102
    
    def parseNetwork(self):
        return self.parseGeneric("NETWORK", self.network)
    
    def parseApp(self):
        self.parseGeneric("APP", self.app)
        
        for key in self.app:
            try:
                self.app[key] = float(self.app[key])
            except:
                pass    
        return self.app

    def parsePatterns(self):
        patterns = self.parseGeneric("PATTERNS", self.patterns)
        for name in patterns:
            patterns[name] = patterns[name].split(',')
        return patterns

    def parseGeneric(self, field, output):
        if not field in self.config.sections():
            log.warning("No %s config found"%(field))
            return output
        for key in self.config[field]:
            output[key] = self.config[field][key]
        #print(output)
        return output
    


if __name__ == "__main__":
    file = "sampleConfig.ini"
    
    config = Configuration(file)
    
    
    