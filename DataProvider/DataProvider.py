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

    @abstractmethod
    def SetRange(self,minlat,maxlat,minlon,maxlon):
        pass

    @abstractmethod
    def SensorAzimuth(self):
        pass

    @abstractmethod
    def SensorZenith(self):
        pass

    @abstractmethod
    def SolarAzimuth(self):
        pass

    @abstractmethod
    def SolarZenith(self):
        pass

    @abstractmethod
    def Dispose(self):
        pass