from DataProvider import *
from HdfOperator import *
import numpy as N

class H8Dataprovider(DataProvider):
    __HdfOperator = HdfOperator()
    __latFileHandle = None
    __lonFileHandle = None
    __DataFileHandle = None
    __fileName = None
    __longitude = None
    __latitude = None
    __startLine = -1
    __endLine  = -1


    def __init__(self):
        super(H8Dataprovider,self).__init__()
        return

    def Dispose(self):
        self.__HdfOperator.Close(self.__lonFileHandle)
        self.__HdfOperator.Close(self.__latFileHandle)
        self.__HdfOperator.Close(self.__DataFileHandle)
        self.__longitude = None
        self.__latitude = None
        return

    def SetFile(self,file):
        self.__latFileHandle = self.__HdfOperator.Open(file[0])
        self.__lonFileHandle = self.__HdfOperator.Open(file[1])
        self.__DataFileHandle = self.__HdfOperator.Open(file[2])
        self.__fileName = file[2]


    def Longitude(self):

        if self.__longitude== None:
            self.__longitude = N.array(self.__HdfOperator.ReadHdfDataset(self.__lonFileHandle, '/', 'Lon'))

        if self.__startLine !=-1 & self.__endLine!=-1:
            return  self.__longitude[self.__startLine:self.__endLine:, :]
        return self.__longitude



    def Latitude(self):

        if self.__latitude== None:
            self.__latitude = N.array(self.__HdfOperator.ReadHdfDataset(self.__latFileHandle, '/', 'Lat'))

        if self.__startLine !=-1 & self.__endLine!=-1:
            return  self.__latitude[self.__startLine:self.__endLine:, :]

        return self.__latitude


    def GetResolution(self):
        return 4000

    def RefData(self,band):
        bandname = ''
        ret = None
        if band == 0:
            bandname = 'NOMChannelVIS0064_4000'
        elif band == 1:
            bandname = 'NOMChannelVIS0086_4000'
        elif band == 2:
            bandname = 'NOMChannelVIS0160_4000'
        elif band == 3:
            bandname = 'NOMChannelVIS0230_4000'

        if bandname!='':

            ret=self.GetDataSet('/', bandname)

        return ret

    def SensorAzimuth(self):

        return self.GetDataSet('/','NOMSatelliteAzimuth')


    def GetDataSet(self,group,ds):

        data = self.__HdfOperator.ReadHdfDataset(self.__DataFileHandle, group, ds)
        ret = None
        if self.__startLine != -1 & self.__endLine != -1:
            ret = data[self.__startLine:self.__endLine:, :]
        else:
            ret = data[:,:]
        return ret

    def SensorZenith(self):
        return self.GetDataSet('/','NOMSatelliteZenith')

    def SolarAzimuth(self):
        return self.GetDataSet('/','NOMSunAzimuth')

    def SolarZenith(self):
        return self.GetDataSet('/','NOMSunZenith')

    def EmissData(self,band):
        return

    def GetFile(self):
        return  self.__fileName

    def SetRange(self,minlat,maxlat,minlon,maxlon):


        lat = self.Latitude()
        rangeIndex = N.where((minlat<=lat) & (lat<=maxlat))

        if rangeIndex[:][0].size<=0:
            return

        self.__startLine = N.min(rangeIndex[:][0])-10
        self.__endLine = N.max(rangeIndex[:][0])+10

        if self.__startLine < 0:
            self.__startLine = 0

        lineCount = lat.shape[0]

        if self.__endLine >= lineCount:
            self.__endLine = lineCount-1


        return


