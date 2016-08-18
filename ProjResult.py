import numpy as N
import ProjOutputData_module as SD

class ProjResult(object):


    def __init__(self):
        super(ProjResult,self).__init__()
        self.U = None
        self.V = None

        self.ResultInfo = None

        self.LatLonRangeMask = None

        self.NeedUpdate = True

        self.__DstProj = None

        self.__Width = 0
        self.__Height = 0
        self.__tv = None
        self.__tu = None
        self.__DataSearchTable = None
        self.__IslatlongProj = False

        self.MaxU = None
        self.MinU = None
        self.MaxV = None
        self.MinV = None

        self.__latlonResRate = float(0.01) / float(1000)
        return

    def SetDstProj(self,dstProj):
        self.__DstProj = dstProj
        if 'latlong' in dstProj.srs:
            self.__IslatlongProj = True

    def Dispose(self):

       del self.U

       del self.V

       del self.ResultInfo

       del self.LatLonRangeMask

       del self.__tv
       del self.__tu
       del self.__DataSearchTable



    # def CalProjectMinMax(self, U, V):
    #
    #     maskU = (U < 999999999)
    #     maskV = (V < 999999999)
    #
    #     RealU = U[maskU]
    #     RealV = V[maskV]
    #     self.MinU = N.min(RealU[:]).astype(N.float32)
    #     self.MinV = N.min(RealV[:]).astype(N.float32)
    #     self.MaxU = N.max(RealU[:]).astype(N.float32)
    #     self.MaxV = N.max(RealV[:]).astype(N.float32)
    #     return self.MinU, self.MinV, self.MaxU, self.MaxV

    # def CalProjectMinMax(self,projRange):

    # def CalCenterUV(self,U,V):
    #     self.CalProjectMinMax(U,V)
    #     centU = (self.MaxU-self.MinU)/2+self.MinU
    #     centV = (self.MaxV-self.MinV)/2+self.MinV
    #     return  centU,centV


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
        tu = (ru-minUF).astype(N.int32)
        tv = (rv-minVF).astype(N.int32)
        return  tu,tv


    def CreateSaveData(self, refdata,resolution,datatype):

        res = resolution
        if self.__IslatlongProj:
            res = self.__latlonResRate*resolution

        if self.NeedUpdate:
            # if self.MaxU == None:
            #     self.CalProjectMinMax(self.U[(self.LatLonRangeMask)], self.V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight( self.MinU, self.MinV, self.MaxU, self.MaxV,res)
            self.__tu, self.__tv = self.CalUVToIJ(res,self.U,self.V,self.MinU,self.MinV)
            self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), self.__tu[(self.LatLonRangeMask)], self.__tv[(self.LatLonRangeMask)])
            self.NeedUpdate = False
        data = refdata[(self.LatLonRangeMask)]
        saveData  = SD.CreateOutputData(int(self.__Width ), int(self.__Height),datatype,self.__DataSearchTable,data)

        del data
        return saveData


