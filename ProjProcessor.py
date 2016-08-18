

from DataOuter.DataOuter import *
from DataProvider.DataProvider import *
from ProjectTransformer import *
from ProjResult import *
import gc

class ProjProcessor(object):

    # __dataProvider = DataProvider()

    # __ProjParam = ProjParameters()
    # __dataOuter = DataOuter()

    # __projResult = ProjResult()

    def __init__(self, dataprovider, dataouter, parameters):
        self.__dataProvider = dataprovider
        self.__ProjParam = parameters
        self.__dataOuter = dataouter
        self.__ProjTransformer = ProjTransformer()
        self.__projResult = ProjResult()

        if self.__ProjParam.ProjectResolution==0:
            self.__ProjParam.ProjectResolution = dataprovider.GetResolution()

        self.__dataProvider.SetParameter(parameters)

        self.__dataOuter.Parameter=parameters

        self.__ProjParam.register(self)

        self.__ProjParam.data_changed()
        return

    def Dispose(self):
        self.__dataProvider.Dispose()
        self.__dataOuter.Dispose()
        self.__projResult.Dispose()
        self.__ProjParam = None

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

        del lon
        del lat
        gc.collect()

        self.__projResult.U = U
        self.__projResult.V = V
        self.__projResult.SetDstProj(proj)

        # self.CalProjRange()
        # centU,centV = self.__projResult.CalCenterUV(U[(rangemask)], V[(rangemask)])

        # centlon,centlat= self.__ProjTransformer.ProjUVToLatlon(centU,centV,proj)

        self.CreateResultInfo()

        self.__dataOuter.Save(self.__projResult,self.__dataProvider)

    def PerformInveProj(self):
        pass

    def CalProjCorner(self):
        minlon = self.__ProjParam.ProjRange.MinLon
        maxlon = self.__ProjParam.ProjRange.MaxLon
        minlat = self.__ProjParam.ProjRange.MinLat
        maxlat = self.__ProjParam.ProjRange.MaxLat
        lon = N.array([minlon,minlon,maxlon,maxlon])
        lat = N.array([minlat,maxlat,minlat,maxlat])

        cornerU,cornerV = self.__ProjTransformer.LatlonToProjUV(lon,lat,self.__ProjParam.DstProj)
        return cornerU,cornerV

    def CalCenterUV(self,MinU, MinV, MaxU, MaxV):
        centU = (MaxU-MinU)/2+MinU
        centV = (MaxV-MinV)/2+MinV
        return  centU,centV

    def CalProjectMinMax(self, U, V):

        MinU = N.min(U[:]).astype(N.float32)
        MinV = N.min(V[:]).astype(N.float32)
        MaxU = N.max(U[:]).astype(N.float32)
        MaxV = N.max(V[:]).astype(N.float32)
        return MinU, MinV, MaxU, MaxV

    def CreateResultInfo(self):
        self.__projResult.ResultInfo={'SatelliteName':self.__dataProvider.OrbitInfo.Sat}
        self.__projResult.ResultInfo['SensorName']=self.__dataProvider.OrbitInfo.Sensor
        self.__projResult.ResultInfo['ProjString'] = self.__ProjParam.GetParamDescription()
        self.__projResult.ResultInfo['UResolution'] = self.__ProjParam.ProjectResolution
        self.__projResult.ResultInfo['VResolution'] = self.__ProjParam.ProjectResolution

        cornerU, cornerV=self.CalProjCorner()
        MinU, MinV, MaxU, MaxV = self.CalProjectMinMax(cornerU,cornerV)
        centU, centV = self.CalCenterUV(MinU, MinV, MaxU, MaxV)
        centlon, centlat = self.__ProjTransformer.ProjUVToLatlon(centU, centV, self.__ProjParam.DstProj)

        self.__projResult.MaxU = MaxU
        self.__projResult.MaxV = MaxV
        self.__projResult.MinV = MinV
        self.__projResult.MinU = MinU
        self.__projResult.ResultInfo['MinLon'] = self.__ProjParam.ProjRange.MinLon
        self.__projResult.ResultInfo['MaxLon'] = self.__ProjParam.ProjRange.MaxLon
        self.__projResult.ResultInfo['MinLat'] = self.__ProjParam.ProjRange.MinLat
        self.__projResult.ResultInfo['MaxLat'] = self.__ProjParam.ProjRange.MaxLat
        self.__projResult.ResultInfo['CenterLatitude'] = centlat
        self.__projResult.ResultInfo['CenterLongitude'] = centlon






