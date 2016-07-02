import sys
from abc import ABCMeta, abstractmethod


class OrbitInfo(object):
    def __init__(self):
        self.Sat = ''
        self.Sensor = ''
        self.OrbitDirection= ''
        self.DNFlag = ''
        self.Date=''
        self.Time=''
        self.BandsCount = 0
        self.Band_name=''
        self.RefSBBandsCount = 0
        self.Width = 0
        self.Height = 0
        self.RefSBBandsNames = ''
        self.EmissiveBandsCoun=0
        self.EmissiveBandsNames = ''


class DataProvider(object):

    def __init__(self):
        return

    __OrbitInfo = OrbitInfo()

    @property
    def OrbitInfo(self):
        return  self.__OrbitInfo


    @abstractmethod
    def GetLongitude(self):
        pass

    @abstractmethod
    def GetLatitude(self):
        pass

    @abstractmethod
    def GetResolution(self):
        pass

    @abstractmethod
    def GetRefData(self, band):
        pass

    @abstractmethod
    def GetEmissData(self, band):
        pass

    @abstractmethod
    def GetFile(self):
        pass

    @abstractmethod
    def SetRange(self,minlat,maxlat,minlon,maxlon):
        pass

    @abstractmethod
    def GetSensorAzimuth(self):
        pass

    @abstractmethod
    def GetSensorZenith(self):
        pass

    @abstractmethod
    def GetSolarAzimuth(self):
        pass

    @abstractmethod
    def GetSolarZenith(self):
        pass

    @abstractmethod
    def Dispose(self):
        pass