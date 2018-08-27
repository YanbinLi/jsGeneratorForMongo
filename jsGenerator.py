
# -*- coding: utf-8 -*- 
import json
import re
class JsGenerator:
    def __init__(self, config):
        config_file = open(config, "r",encoding="utf-8")
        config_json = config_file.read()
        config_file.close()
        jsonObject = json.loads(config_json)
        self.configs = jsonObject

    
    def generatorJs(self):
        for config in self.configs:
            match = self.__generateMatch(config.match)
            unwind = self.__generateUnwind(config.items) 


    def __generateMatch(self, match):

        ele = match.split(" ")

        return ""
    
    def __exical_analysis(self, input):
        """词法分析器"""
        input = re.sub(r"\s+", " ", a)
        

    

    def __generateUnwind(self, items):
        return ""
    def __generateProject(self, items):
        return ""
    def __generateGroup(self, group):
        return ""
    def __generatePrint(self, items):
        return ""

        

if __name__ == "__main__":
    a = "a b   c           \n  d" 
    print(a)
    b = re.sub(r"\s+", " ", a)
    print(b)

    