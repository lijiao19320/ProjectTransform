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

        minU, minV, maxU, maxV,maskU,maskV=self.CalProjectMinMax(U,V)
        resolution =self.__dataProvider.GetResolution()
        Height, Width = self.CalProjectWidthAndHeight( minU, minV, maxU, maxV,resolution)
        savefile = '/mnt/hgfs/Vmware Linux/Data/save.hdf'
        if os.path.exists(savefile):
            os.remove(savefile)

        refdata = self.__dataProvider.RefData(0)
        savdData=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,refdata,maskU,maskV)


        fileHandle = self.__HdfOperator.Open(savefile)

        self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'EVB_Ref', savdData)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, 'tt', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, 'tt', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def CalProjectMinMax(self,U,V):
        maskU = (U[:,:]< 999999999)
        maskV = (V[:,:]< 999999999)

        RealU = U[maskU]
        RealV = V[maskV]
        minU = N.min(RealU[:])
        minV = N.min(RealV[:])
        maxU = N.max(RealU[:])
        maxV = N.max(RealV[:])
        return  minU,minV,maxU,maxV,maskU,maskV

    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):


        Height = round((maxV- minV) / resolution+ 0.5)
        Width = round((maxU- minU) / resolution+ 0.5)

        return Height,Width

    def CreateSaveData(self,minU, minV,width,height,U,V,resolution,refdata,maskU,maskV):
        saveData = N.ones((height,width))*400
        UVshape = U.shape
        resolutionFactor = float(1)/float(resolution)
        ru = U*resolutionFactor
        rv = V*resolutionFactor
        minUF = minU*resolutionFactor
        minVF = minV*resolutionFactor
        tu = (ru-minUF).astype(int)
        tv = (rv-minVF).astype(int)

        icount = UVshape[0]
        jcount = UVshape[1]
        for i in range(icount):
            for j in range(jcount):
                if (maskU[i,j] != True):
                    continue

                posX = tu[i,j]
                posY = tv[i,j]
                # saveData[posY,posX] = refdata[i,j]
        return saveData