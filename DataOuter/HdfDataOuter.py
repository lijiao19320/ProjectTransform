from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N
import cos_module_np as SD


class HdfDataOuter(DataOuter):

    __HdfOperator = HdfOperator()

    __dataProvider = DataProvider()

    def __init__(self):
        super(HdfDataOuter, self).__init__()
        return


    def Save(self,projResult, dataProvider):
        self.__dataProvider = dataProvider
        U = projResult.U
        V = projResult.V
        minU, minV, maxU, maxV,maskU,maskV=self.CalProjectMinMax(U,V)
        resolution =self.__dataProvider.GetResolution()
        Height, Width = self.CalProjectWidthAndHeight( minU, minV, maxU, maxV,resolution)
        savefilePath = self.__dataProvider.GetFile()

        savePath,saveFile =  os.path.split(savefilePath)
        saveFile = saveFile.upper()
        saveFile=saveFile.replace('.HDF','Proj.HDF')

        savefilePath = savePath+'/'+saveFile
        if os.path.exists(savefilePath):
            os.remove(savefilePath)

        fileHandle = self.__HdfOperator.Open(savefilePath)

        refdata = self.__dataProvider.GetRefData(0)
        if refdata != None:
            savdrefData=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,refdata)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'EVB_Ref', savdrefData)

        sensorAzimuthdata = self.__dataProvider.GetSensorAzimuth()
        if sensorAzimuthdata!=None:
            savesensorAzimuthdata=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,sensorAzimuthdata)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'SensorAzimuth', savesensorAzimuthdata)

        sensorZenithdata = self.__dataProvider.GetSensorZenith()
        if sensorZenithdata!=None:
            savesensorZenithdata=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,sensorZenithdata)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'SensorZenith', savesensorZenithdata)

        solarAzimuthdata = self.__dataProvider.GetSolarAzimuth()
        if solarAzimuthdata!=None:
            savesolarAzimuthdata=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,solarAzimuthdata)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'SolarAzimuth', savesolarAzimuthdata)


        solarZenithdata = self.__dataProvider.GetSolarZenith()
        if solarZenithdata!=None:
            savesoarZenithdata=self.CreateSaveData(minU, minV,Width,Height,U,V,resolution,solarZenithdata)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'SolarZenith', savesoarZenithdata)

        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return


    def WriteAttribute(self):

        return


    def CalProjectMinMax(self,U,V):
        maskU = (U[:,:]< 999999999)
        maskV = (V[:,:]< 999999999)

        RealU = U[maskU]
        RealV = V[maskV]
        minU = N.min(RealU[:])
        minV = N.min(RealV[:])
        maxU = N.max(RealU[:])
        maxV = N.max(RealV[:])
        return  minU,minV,maxU,maxV,maskU,maskV
    #
    # def LonLatBox(self, lat, lon):
    #     masklat = (lat[:,:] <= 90) & (lat[:,:]>=-90)
    #     masklon = (lon[:, :] <= 180) & (lon[:, :] >= -180)
    #     latitude = lat[masklat]
    #     longitude = lon[masklon]
    #
    #     minlat = N.min(latitude)
    #     minlon = N.min(longitude)
    #     maxlat  = N.max(latitude)
    #     maxlon = N.max(longitude)
    #
    #     print minlat,minlon,maxlat,maxlon
    #
    #     lon = N.array([minlon,minlon,maxlon,maxlon])
    #     lat = N.array([maxlat,minlat,maxlat,minlat])
    #     proj = self.__ProjParam.DstProj
    #     boxUV = self.__ProjTransformer.LatlonToProjUV(lon, lat, proj)
    #
    #     print  boxUV

    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):


        Height = round((maxV- minV) / resolution+ 0.5)
        Width = round((maxU- minU) / resolution+ 0.5)

        return Height,Width

    def CreateSaveData(self,minU, minV,width,height,U,V,resolution,refdata):
        # saveData = N.ones((height,width))*400
        UVshape = U.shape
        resolutionFactor = float(1)/float(resolution)
        ru = U*resolutionFactor
        rv = V*resolutionFactor
        minUF = minU*resolutionFactor
        minVF = minV*resolutionFactor
        tu = (ru-minUF).astype(int)
        tv = (rv-minVF).astype(int)

        # icount = UVshape[0]
        # jcount = UVshape[1]

        saveData = SD.cos_func_np(int(width), int(height), tu, tv, refdata.astype(int))

        # for i in range(icount):
        #     for j in range(jcount):
        #         if (maskU[i,j] != True):
        #             continue
        #
        #         posX = tu[i,j]
        #         posY = tv[i,j]
        #         saveData[posY,posX] = refdata[i,j]

        # print N.max(refdata),N.min(refdata)
        # savemask = (saveData[:,:]==0)

        return saveData