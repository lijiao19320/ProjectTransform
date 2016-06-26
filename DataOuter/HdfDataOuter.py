from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N

class HdfDataOuter(DataOuter):

    __HdfOperator = HdfOperator()

    __dataProvider = DataProvider()

    def __init__(self):
        super(HdfDataOuter, self).__init__()
        return


    def Save(self,U,V, dataProvider):
        self.__dataProvider = dataProvider

        minU, minV, maxU, maxV=self.CalProjectMinMax(U,V)
        Height, Width = self.CalProjectWidthAndHeight( minU, minV, maxU, maxV,self.__dataProvider.GetResolution())
        savefile = '/mnt/hgfs/Vmware Linux/Data/save.hdf'
        if os.path.exists(savefile):
            os.remove(savefile)
        refdata = self.__dataProvider.RefData(1)
        self.CreateSaveData(minU, minV,Width,Height,U,V,refdata)


        fileHandle = self.__HdfOperator.Open(savefile)
        self.__HdfOperator.WriteHdfDataset(fileHandle, 'tt', 'U', U)
        self.__HdfOperator.WriteHdfDataset(fileHandle, 'tt', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def CalProjectMinMax(self,U,V):
        maskU = (U[:,:]< 99999999)
        maskV = (V[:,:]< 99999999)

        RealU = U[maskU]
        RealV = V[maskV]
        minU = N.min(RealU[:])
        minV = N.min(RealV[:])
        maxU = N.max(RealU[:])
        maxV = N.max(RealV[:])
        return  minU,minV,maxU,maxV

    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):


        Height = (maxV- minV) / resolution+ 0.5
        Width = (maxU- minU) / resolution+ 0.5

        return Height,Width

    def CreateSaveData(self,minU, minV,width,height,resolution,U,V,refdata):
        saveData = N.zeros((height,width))

        print saveData
        return