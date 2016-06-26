from pyproj import Proj, transform
from Parameters import *
from math import *
import numpy as N

class ProjTransformer(object):
    RAD2DEG = 180.0 / pi
    DEG2RAD = pi/ 180.0

    def LatlonToProjUV (self, lon, lat, dstproj):
        U=[]
        V=[]
        srcProj =Proj(proj='latlong',datum='WGS84')
        if lon.ndim == 1 :

            # projUV = dstproj(lon[:]*self.DEG2RAD, lat[:]*self.DEG2RAD)l
            U,V = self.ProjectTransform(lon[:]*self.DEG2RAD,lat[:]*self.DEG2RAD,srcProj,dstproj)
        elif lon.ndim == 2:
            # projUV = dstproj(lon[:, :] * self.DEG2RAD, lat[:, :] * self.DEG2RAD)
            U, V = self.ProjectTransform(lon[:, :] * self.DEG2RAD, lat[:, :]* self.DEG2RAD, srcProj, dstproj)

        return U,V

    def ProjectTransform(self,Xsrc,Ysrc,srcProj,dstProj):

        Zsrc = N.zeros(Xsrc.shape)
        Xdest,Ydest,Zdest = transform(srcProj, dstProj, Xsrc, Ysrc,Zsrc,6378137)
        # result = N.array(Xdest,Ydest)

        return Xdest,Ydest

