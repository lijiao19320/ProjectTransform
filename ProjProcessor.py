

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
        resolution = self.__dataProvider.GetResolution()
        # minlat, maxlat, minlon, maxlon=self.LonLatBox(lat, lon)
        # self.CalProjectWidthAndHeight(minlat,maxlat,minlon,maxlon,self.__resolution)
        # self.LonLatBox(lat,lon)
        proj = self.__ProjParam.DstProj
        U, V = self.__ProjTransformer.LatlonToProjUV(lon,lat,proj)
        # self.CalProjectWidthAndHeight(U,V, resolution)
        self.__dataOut.Save(U,V,self.__dataProvider)

    def LonLatBox(self, lat, lon):
        masklat = (lat[:,:] <= 90) & (lat[:,:]>=-90)
        masklon = (lon[:, :] <= 180) & (lon[:, :] >= -180)
        latitude = lat[masklat]
        longitude = lon[masklon]

        minlat = N.min(latitude)
        minlon = N.min(longitude)
        maxlat  = N.max(latitude)
        maxlon = N.max(longitude)

        print minlat,minlon,maxlat,maxlon

        lon = N.array([minlon,minlon,maxlon,maxlon])
        lat = N.array([maxlat,minlat,maxlat,minlat])
        proj = self.__ProjParam.DstProj
        boxUV = self.__ProjTransformer.LatlonToProjUV(lon, lat, proj)

        print  boxUV








