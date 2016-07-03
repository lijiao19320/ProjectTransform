

from DataOuter.DataOuter import *
from DataProvider.DataProvider import *
from ProjectTransformer import *
from ProjResult import *

class ProjProcessor(object):

    __dataProvider = DataProvider()
    __ProjTransformer = ProjTransformer()
    __ProjParam = ProjParameters()
    __dataOuter = DataOuter()

    __projResult = ProjResult()



    def SetDataProvider(self,provider):
        self.__dataProvider = provider


    def SetProjParameters(self,parameters):
        self.__ProjParam = parameters

    def SetDataOut(self,out):
        self.__dataOuter = out


    def PerformProj(self):
        lat = self.__dataProvider.GetLatitude()
        lon = self.__dataProvider.GetLongitude()

        proj = self.__ProjParam.DstProj
        U, V = self.__ProjTransformer.LatlonToProjUV(lon,lat,proj)

        self.__projResult.U = U
        self.__projResult.V = V


        self.CreateResultInfo();
        self.__dataOuter.Save(self.__projResult,self.__dataProvider)


    def CreateResultInfo(self):
        self.__projResult.ResultInfo={'Satellite Name':self.__dataProvider.OrbitInfo.Sat}
        self.__projResult.ResultInfo['Sensor Name']=self.__dataProvider.OrbitInfo.Sensor







