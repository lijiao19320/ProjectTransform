from DataProvider import *
from HdfOperator import *

class FY3AVirrProvider(DataProvider):

    __HdfOperator = HdfOperator()

    __fileName = None

    __filehandel=None

    __RefData = None


    def __init__(self):
        super(FY3AVirrProvider,self).__init__()
        return

    def Dispose(self):
        return

    def SetFile(self,file):

        self.__filehandel = self.__HdfOperator.Open(file)

    def GetFile(self):
        return  self.__fileName


    def Longitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Longitude')



    def Latitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Latitude')

    def SensorAzimuth(self):
        return

    def SensorZenith(self):
        return

    def SolarAzimuth(self):
        return

    def SolarZenith(self):
        return

    def RefData(self,band):
        if self.__RefData == None:
            self.__RefData = self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'EV_RefSB')
        return self.__RefData[band,:,:]

    def GetResolution(self):
        return 1000

    def SetRange(self,minlat,maxlat,minlon,maxlon):

        return