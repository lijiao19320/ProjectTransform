from pyproj import Proj, transform

class ProjParameters(object):

    SrcProj = Proj(proj='longlat',ellps='WGS84')

    DstProj = Proj(proj='lcc',ellps='WGS84')

    # def getV(self):
    #     return self.__V
    #
    # def setV(self, value):
    #     self.__V = value
    #
    # V = property(getV, setV)

    __ProjRange = {0,0,0,0}

    def SetProjRange(self,minlat,maxlat,minlon,maxlon):
        self.__ProjRange = {minlat,maxlat,minlon,maxlon}
        return

