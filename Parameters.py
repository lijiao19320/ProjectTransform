from pyproj import Proj, transform
from abc import ABCMeta, abstractmethod

class ProjRange(object):
    def __init__(self,minlat,maxlat,minlon,maxlon):
        self.MinLat = minlat
        self.MaxLat = maxlat
        self.MinLon = minlon
        self.MaxLon = maxlon




class ProjParameters(object):

    def __init__(self):
        self.observers = []

    def register(self, observer):
        if observer not in self.observers:
            if  'OnParametersUpdate' in dir(observer):
                self.observers.append(observer)
            else:
                raise Exception('OnParametersUpdate Not Define!')

    def deregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for o in self.observers:
            o.OnParametersUpdate()

    def data_changed(self):
        self.notify_observers()


    __SrcProj = Proj(proj='longlat',ellps='WGS84')
    def setSrcProj(self,scrProj):
        self.__SrcProj = scrProj


    def getSrcProj(self):
        return  self.__SrcProj

    SrcProj = property(getSrcProj,setSrcProj)



    __DstProj = Proj(proj='lcc',ellps='WGS84')
    def setDstProj(self,dstproj):
        self.__DstProj = dstproj

    def getDstProj(self):
        return  self.__DstProj

    DstProj = property(getDstProj,setDstProj)



    __ProjRange = ProjRange(-90,90,-180,180)

    def setProjRange(self,projrange):
        self.__ProjRange = projrange

    def getProjRange(self):
        return  self.__ProjRange

    ProjRange = property(getProjRange,setProjRange)

