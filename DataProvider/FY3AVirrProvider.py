from DataProvider import *
from HdfOperator import *

class FY3AVirrProvider(DataProvider):

    __HdfOperator = HdfOperator()

    __fileName = None

    __filehandel=None

    __RefData = None

    __minlat = None
    __maxlat = None
    __minlon = None
    __maxlon = None

    def __init__(self):
        super(FY3AVirrProvider,self).__init__()
        return

    def SetFile(self,file):

        self.__filehandel = self.__HdfOperator.Open(file)

    def GetFile(self):
        return  self.__fileName


    def Longitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Longitude')



    def Latitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Latitude')

    def RefData(self,band):
        if self.__RefData == None:
            self.__RefData = self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'EV_RefSB')
        return self.__RefData[band,:,:]

    def GetResolution(self):
        return 1000

    def SetRange(self,minlat,maxlat,minlon,maxlon):
        self.__minlat = minlat
        self.__maxlat = maxlat
        self.__minlon = minlon
        self.__maxlon = maxlon
        return