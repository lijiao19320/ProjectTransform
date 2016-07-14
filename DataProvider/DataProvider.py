import sys
from abc import ABCMeta, abstractmethod
import numpy as N

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

    startLine = -1
    endLine  = -1
    __parameter = None

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
    def GetOBSData(self, band):
        pass

    @abstractmethod
    def GetOBSDataCount(self):
        pass
    # @abstractmethod
    # def GetEmissData(self, band):
    #     pass

    @abstractmethod
    def GetFile(self):
        pass

    # @abstractmethod
    # def SetParameter(self, papameter):
    #     pass

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

    def SetParameter(self, parameter):
        parameter.register(self)
        self.__parameter = parameter

        return

    def OnParametersUpdate(self):
        lat = self.GetLatitude()
        minlat = self.__parameter.ProjRange.MinLat
        maxlat = self.__parameter.ProjRange.MaxLat
        rangeIndex = N.where((minlat<=lat) & (lat<=maxlat))

        if rangeIndex[:][0].size<=0:
            return

        self.startLine = N.min(rangeIndex[:][0])-10
        self.endLine = N.max(rangeIndex[:][0])+10

        if self.startLine < 0:
            self.startLine = 0

        lineCount = lat.shape[0]

        if self.endLine >= lineCount:
            self.endLine = lineCount-1
        return
