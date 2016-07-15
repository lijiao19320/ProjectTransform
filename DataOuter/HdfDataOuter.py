from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N


class HdfDataOuter(DataOuter):

    __HdfOperator = HdfOperator()

    __dataProvider = DataProvider()

    def __init__(self):
        super(HdfDataOuter, self).__init__()
        return


    def Save(self,projResult, dataProvider):
        self.__dataProvider = dataProvider

        resolution = self.__dataProvider.GetResolution()
        para = self.getParameter()

        savefile = self.__dataProvider.GetFile()

        savePath,saveFile =  os.path.split(savefile)
        saveFile = saveFile.upper()
        saveFile=saveFile.replace('.HDF','_Proj.HDF')

        savefile = para.OutputPath+saveFile
        if os.path.exists(savefile):
            os.remove(savefile)

        fileHandle = self.__HdfOperator.Open(savefile)


        Evbcnt = dataProvider.GetOBSDataCount()+1
        for i in xrange(1,Evbcnt):
            self.WriteData('EVB'+str(i),projResult,fileHandle,resolution)



        # self.WriteData('SensorAzimuth', projResult, fileHandle, resolution)

        # self.__HdfOperator.Close(fileHandle)
        # return
        #
        # self.WriteData('SensorZenith', projResult, fileHandle, resolution)
        # self.WriteData('SolarAzimuth', projResult, fileHandle, resolution)
        # self.WriteData('SolarZenith', projResult, fileHandle, resolution)

        for attr in projResult.ResultInfo.keys():
            self.__HdfOperator.WriteHdfAttribute(fileHandle,attr,projResult.ResultInfo[attr])
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def WriteData(self,datasetname,projResult,fileHandle,resolution):
        data = None
        datatype =0
        if 'EVB' in datasetname:
            data = (self.__dataProvider.GetOBSData(datasetname)).astype(N.int32)

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


