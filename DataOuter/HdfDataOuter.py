from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N

from scipy.interpolate import griddata
from scipy.weave import inline
from scipy.weave import converters

class HdfDataOuter(DataOuter):

    __HdfOperator = HdfOperator()

    __dataProvider = DataProvider()

    def __init__(self):
        super(HdfDataOuter, self).__init__()
        return


    def Save(self,projResult, dataProvider):
        self.__dataProvider = dataProvider

        resolution = self.__dataProvider.GetResolution()
        savefilePath = self.__dataProvider.GetFile()

        savePath,saveFile =  os.path.split(savefilePath)
        saveFile = saveFile.upper()
        saveFile=saveFile.replace('.HDF','Proj.HDF')

        savefilePath = savePath+'/'+saveFile
        if os.path.exists(savefilePath):
            os.remove(savefilePath)

        fileHandle = self.__HdfOperator.Open(savefilePath)


        self.WriteData('EVB_Ref',projResult,fileHandle,resolution)
        # self.WriteData('EVB_Ref1', projResult, fileHandle, resolution)
        # self.WriteData('EVB_Ref2', projResult, fileHandle, resolution)
        # self.WriteData('EVB_Ref3', projResult, fileHandle, resolution)


        self.WriteData('SensorAzimuth', projResult, fileHandle, resolution)

        # self.__HdfOperator.Close(fileHandle)
        # return

        self.WriteData('SensorZenith', projResult, fileHandle, resolution)
        self.WriteData('SolarAzimuth', projResult, fileHandle, resolution)
        self.WriteData('SolarZenith', projResult, fileHandle, resolution)

        for attr in projResult.ResultInfo.keys():
            self.__HdfOperator.WriteHdfAttribute(fileHandle,attr,projResult.ResultInfo[attr])
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def WriteData(self,datasetname,projResult,fileHandle,resolution):
        data = None
        datatype =0
        if datasetname == 'EVB_Ref':
            data = (self.__dataProvider.GetRefData(0)).astype(N.int32)
        if datasetname == 'EVB_Ref1':
            data = (self.__dataProvider.GetRefData(1)).astype(N.int32)
        if datasetname == 'EVB_Ref2':
            data = (self.__dataProvider.GetRefData(2)).astype(N.int32)
        if datasetname == 'EVB_Ref3':
            data = (self.__dataProvider.GetRefData(3)).astype(N.int32)
        elif datasetname == 'SensorAzimuth':
            data = (self.__dataProvider.GetSensorAzimuth()).astype(N.float32)
            datatype=1
        elif datasetname == 'SensorZenith':
            data = (self.__dataProvider.GetSensorZenith()).astype(N.float32)
            datatype=1
        elif datasetname == 'SolarAzimuth':
            data = (self.__dataProvider.GetSolarAzimuth()).astype(N.float32)
            datatype=1
        elif datasetname == 'SolarZenith':
            data = (self.__dataProvider.GetSolarZenith()).astype(N.float32)
            datatype=1

        U = projResult.U
        V = projResult.V
        if data != None:
            savedata = projResult.CreateSaveData(U, V, data,resolution,datatype)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata)
            print 'Save '+datasetname

    def WriteAttribute(self,projResult):

        return


