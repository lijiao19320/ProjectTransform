import sys
from abc import ABCMeta, abstractmethod


class DataProvider(object):

    def __init__(self):
        return

    @abstractmethod
    def Longitude(self):
        pass

    @abstractmethod
    def Latitude(self):
        pass

    @abstractmethod
    def GetResolution(self):
        pass

    @abstractmethod
    def RefData(self,band):
        pass

    @abstractmethod
    def EmissData(self,band):
        pass

    @abstractmethod
    def GetFile(self):
        pass