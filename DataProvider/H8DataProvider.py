from DataProvider import *
from HdfOperator import *

class H8Dataprovider(DataProvider):
    __HdfOperator = HdfOperator()
    __latFile = ''
    __lonFile = ''
    __fileName = None

    def __init__(self):
        super(H8Dataprovider,self).__init__()
        return

    def SetFile(self,file):
        self.__latFile = file[0]
        self.__lonFile = file[1]


    def Longitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__lonFile, '/', 'Lon')



    def Latitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__latFile, '/', 'Lat')

    def GetResolution(self):
        return 4000

    def RefData(self,band):
        return

    def EmissData(self,band):
        return

    def GetFile(self):
        return  self.__fileName