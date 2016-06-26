from DataProvider import *
from HdfOperator import *

class FY3AVirrProvider(DataProvider):

    __HdfOperator = HdfOperator()


    __filehandel=None

    __RefData = None

    def __init__(self):
        super(FY3AVirrProvider,self).__init__()
        return

    def SetFile(self,file):

        self.__filehandel = self.__HdfOperator.Open(file)


    def Longitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Longitude')



    def Latitude(self):
        return self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'Latitude')

    def RefData(self,band):
        if self.__RefData == None:
            self.__RefData = self.__HdfOperator.ReadHdfDataset(self.__filehandel, '/', 'EV_RefSB')
        return self.__RefData[band,:,:]

    def GetResolution(self):
        return 500