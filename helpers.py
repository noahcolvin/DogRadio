import re

class Parser():
    @staticmethod
    def parseVolume(value):
        pattern = re.compile('volume:[\s\d]{3}%')
        match = pattern.findall(value)
        if match:
            volume = match[0].split(":");
            if volume[0] == "volume":
                return volume[1].replace(' ','').replace('%','')
        return value

    @staticmethod
    def parsePlayMode(value):
        pattern = re.compile('\[[a-z]*\]')
        match = pattern.findall(value)
        if match:
            mode = match[0].replace('[','').replace(']','');
            return mode
        return 'stopped'

    @staticmethod
    def parseTitle(value):
        lines = value.split('\n')
        if len(lines) == 4:
            return lines[0]
        return 'none'
