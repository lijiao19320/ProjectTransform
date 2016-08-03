import xml.etree.ElementTree as ET
from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *

class ParameterParser(object):
    def parseXML(self,xmlfile):
        tree = ET.parse(xmlfile)
        root = tree.getroot()

        __minlat = 0
        __minlon = 0
        __maxlat = 0
        __maxlon = 0
        __resolution = 0
        __CentralLon = 0
        __method = None
        __format = None
        __TaskName = None

        for ProjInfor in root.iter('ProjInfor'):
            self.__format = ProjInfor.find('ProjFormat').text
            self.__TaskName = ProjInfor.find('ProjTaskName').text
            self.__method = ProjInfor.find('ProjMethod').text
            self.__resolution = ProjInfor.find('Resolution').text
            self.__CentralLon = ProjInfor.find('CentralLon').text

        for projrange in root.iter('ProjRange'):
            self.__maxlon = projrange.find('MaxLon').text
            self.__minlon = projrange.find('MinLon').text
            self.__maxlat = projrange.find('MaxLat').text
            self.__minlat = projrange.find('MinLat').text

        param = ProjParameters()
        param.ProjRange = ProjRange(int(self.__minlat),int(self. __maxlat), int(self.__minlon), int(self.__maxlon))
        param.DstProj = Proj(proj=self.__method, datum='WGS84', lon_0=int(self.__CentralLon))

        return param