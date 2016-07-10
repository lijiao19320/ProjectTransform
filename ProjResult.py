import numpy as N
import ProjOutputData_module as SD

class ProjResult(object):

    U = None
    V = None

    ResultInfo = None

    LatLonRangeMask = None

    NeedUpdate = True

    __Width = 0
    __Height =0
    __tv = None
    __tu = None
    __DataSearchTable = None

    def CalProjectMinMax(self, U, V):

        maskU = (U < 999999999)
        maskV = (V < 999999999)

        RealU = U[maskU]
        RealV = V[maskV]
        minU = N.min(RealU[:])
        minV = N.min(RealV[:])
        maxU = N.max(RealU[:])
        maxV = N.max(RealV[:])
        return minU, minV, maxU, maxV

    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):


        Height = round((maxV- minV) / resolution+ 0.5)
        Width = round((maxU- minU) / resolution+ 0.5)

        return Height,Width

    def CalUVToIJ(self,resolution,U,V,minU,minV):
        resolutionFactor = float(1)/float(resolution)
        ru = U*resolutionFactor
        rv = V*resolutionFactor
        minUF = minU*resolutionFactor
        minVF = minV*resolutionFactor
        tu = (ru-minUF).astype(int)
        tv = (rv-minVF).astype(int)
        return  tu,tv


    def CreateSaveData(self, U, V, refdata,resolution,datatype):

        if self.NeedUpdate:
            minU, minV, maxU, maxV=self.CalProjectMinMax(U[(self.LatLonRangeMask)], V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight( minU, minV, maxU, maxV,resolution)
            self.__tu, self.__tv = self.CalUVToIJ(resolution,U,V,minU,minV)
            self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), self.__tu[(self.LatLonRangeMask)], self.__tv[(self.LatLonRangeMask)])
            self.NeedUpdate = False

        saveData  = SD.CreateOutputData(int(self.__Width ), int(self.__Height),datatype,self.__DataSearchTable,refdata[(self.LatLonRangeMask)])

        return saveData

