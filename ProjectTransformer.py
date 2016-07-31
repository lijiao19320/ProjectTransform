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

        if 'latlong' in dstproj.srs:
           return  lon,lat

        if lon.ndim == 1 :
            # U,V = self.ProjectTransform(lon[:]*self.DEG2RAD,lat[:]*self.DEG2RAD,srcProj,dstproj)
            U, V = dstproj(lon[:],lat[:])
        elif lon.ndim == 2:
            # U, V = self.ProjectTransform(lon[:, :] * self.DEG2RAD, lat[:, :]* self.DEG2RAD, srcProj, dstproj)
            U, V = dstproj(lon[:,:] , lat[:,:] )
        return U,V


    def ProjectTransform(self,Xsrc,Ysrc,srcProj,dstProj):


        Zsrc = N.zeros(Xsrc.shape)
        Xdest,Ydest,Zdest = transform(srcProj, dstProj, Xsrc, Ysrc,Zsrc,6378137)

        return Xdest,Ydest

    def ProjUVToLatlon(self,U,V,srcProj):
        lon = None
        lat = None
        dstProj = Proj(proj='latlong', datum='WGS84')
        if 'latlong' in srcProj.srs:
            return U, V

        if type(U) == N.ndarray:
            if lon.ndim == 1 :
                # lon,lat = self.ProjectTransform(U[:],V[:],srcProj,dstProj)
                lon,lat = srcProj(U[:],V[:],inverse=True)
            elif lon.ndim == 2:
                # lon, lat = self.ProjectTransform(U[:, :], V[:, :], srcProj, dstProj)
                lon, lat = srcProj(U[:,:], V[:,:], inverse=True)
        else:
            lon, lat = srcProj(U,V,inverse=True)

        return lon,lat