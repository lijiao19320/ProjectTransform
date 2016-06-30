

from DataOuter.DataOuter import *
from DataProvider.DataProvider import *
from ProjectTransformer import *


class ProjProcessor(object):

    __dataProvider = DataProvider()
    __ProjTransformer = ProjTransformer()
    __ProjParam = ProjParameters()
    __dataOut = DataOuter()





    def SetDataProvider(self,provider):
        self.__dataProvider = provider


    def SetProjParameters(self,parameters):
        self.__ProjParam = parameters

    def SetDataOut(self,out):
        self.__dataOut = out


    def PerformProj(self):
        lat = self.__dataProvider.Latitude()
        lon = self.__dataProvider.Longitude()

        proj = self.__ProjParam.DstProj
        U, V = self.__ProjTransformer.LatlonToProjUV(lon,lat,proj)

        self.__dataOut.Save(U,V,self.__dataProvider)










