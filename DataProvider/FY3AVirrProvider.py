from DataProvider import *
from HdfOperator import *

class FY3AVirrProvider(DataProvider):

    __HdfOperator = HdfOperator()

    __fileName = None

    __filehandel=None

    __RefData = None

    __longitude = None
    __latitude = None
    __startLine = -1
    __endLine  = -1


    def __init__(self):
        super(FY3AVirrProvider,self).__init__()
        return

    def Dispose(self):
        return

    def SetFile(self,file):

        self.__filehandel = self.__HdfOperator.Open(file)
        self.__fileName = file

    def GetFile(self):
        return  self.__fileName


    def GetLongitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Longitude')



    def GetLatitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Latitude')

    def GetSensorAzimuth(self):
        return

    def GetSensorZenith(self):
        return

    def GetSolarAzimuth(self):
        return

    def GetSolarZenith(self):
        return

    def GetRefData(self, band):
        if self.__RefData == None:
            self.__RefData = self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'EV_RefSB')
        return self.__RefData[band,:,:]

    def GetResolution(self):
        return 1000

    # def SetParameter(self, papameter):
    #
    #     return