

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

    def __init__(self, dataprovider, dataouter, parameters):
        self.__dataProvider = dataprovider
        self.__ProjParam = parameters
        self.__dataOuter = dataouter

        if self.__ProjParam.ProjectResolution==0:
            self.__ProjParam.ProjectResolution = dataprovider.GetResolution()

        self.__dataProvider.SetParameter(parameters)

        self.__dataOuter.Parameter=parameters

        self.__ProjParam.register(self)

        self.__ProjParam.data_changed()
        return


    def OnParametersUpdate(self):
        self.__projResult.NeedUpdate = True
        return


    def PerformProj(self):
        lat = self.__dataProvider.GetLatitude()
        lon = self.__dataProvider.GetLongitude()


        rangemask =(lat[:,:]<= self.__ProjParam.ProjRange.MaxLat) & (lat[:,:]>= self.__ProjParam.ProjRange.MinLat) & \
                 (lon[:,:]<= self.__ProjParam.ProjRange.MaxLon) & (lon[:,:]>= self.__ProjParam.ProjRange.MinLon)


        self.__projResult.LatLonRangeMask = rangemask

        proj = self.__ProjParam.DstProj
        U, V = self.__ProjTransformer.LatlonToProjUV(lon,lat,proj)

        self.__projResult.U = U
        self.__projResult.V = V


        self.CreateResultInfo()
        self.__dataOuter.Save(self.__projResult,self.__dataProvider)


    def CreateResultInfo(self):
        self.__projResult.ResultInfo={'Satellite Name':self.__dataProvider.OrbitInfo.Sat}
        self.__projResult.ResultInfo['Sensor Name']=self.__dataProvider.OrbitInfo.Sensor







