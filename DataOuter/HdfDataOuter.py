from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N
import gc

class HdfDataOuter(DataOuter):

    __HdfOperator = HdfOperator()

    __dataProvider = DataProvider()

    def __init__(self):
        super(HdfDataOuter, self).__init__()
        return

    def Dispose(self):
        self.__dataProvider = None

    def Save(self,projResult, dataProvider):
        self.__dataProvider = dataProvider


        para = self.getParameter()
        resolution = para.ProjectResolution

        dataDescription = self.__dataProvider.GetDataDescription()

        # savePath,saveFile =  os.path.split(savefile)
        # saveFile = saveFile.upper()
        # saveFile=saveFile.replace('.HDF','_Proj.HDF')

        saveFile = para.OutputPath+dataDescription+'_'+para.ProjectTaskName+'.HDF'


        if os.path.exists(saveFile):
            os.remove(saveFile)

        fileHandle = self.__HdfOperator.Open(saveFile)



        Evbcnt = dataProvider.GetOBSDataCount()+1
        for i in xrange(1,Evbcnt):
            self.WriteDataset('EVB' + str(i), projResult, fileHandle, resolution)
            self.WriteDatasetAttribute(fileHandle,'EVB' + str(i))

        AuxiliaryDataNamesList=dataProvider.GetAuxiliaryDataNamesList()
        for auxName in AuxiliaryDataNamesList:
            self.WriteDataset(auxName, projResult, fileHandle, resolution)
        # self.WriteData('SensorAzimuth', projResult, fileHandle, resolution)

        # self.__HdfOperator.Close(fileHandle)
        # return
        #
        # self.WriteData('SensorZenith', projResult, fileHandle, resolution)
        # self.WriteData('SolarAzimuth', projResult, fileHandle, resolution)
        # self.WriteData('SolarZenith', projResult, fileHandle, resolution)

        for attr in projResult.ResultInfo.keys():
            self.__HdfOperator.WriteHdfGroupAttribute(fileHandle, attr, projResult.ResultInfo[attr])
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'U', U)
        # self.__HdfOperator.WriteHdfDataset(fileHandle, '/', 'V', V)
        self.__HdfOperator.Close(fileHandle)
        return

    def WriteDataset(self, datasetname, projResult, fileHandle, resolution):
        data = None
        datatype =0
        if 'EVB' in datasetname:
            data = (self.__dataProvider.GetOBSData(datasetname)).astype(N.int32)
        else:
            data = self.__dataProvider.GetAuxiliaryData(datasetname)
            if (data.dtype == N.float)|(data.dtype == N.float32)|(data.dtype == N.float64):
                data = data.astype(N.float32)
                datatype = 1
            else:
                data = data.astype(N.int32)

        if data is not None:
            savedata = projResult.CreateSaveData(data,resolution,datatype)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata)
            del data
            del savedata
            gc.collect()
            print 'Save '+ str(resolution)+'M'+datasetname

    def WriteDatasetAttribute(self,fileHandle,datasetname):
        if 'EVB' in datasetname:
            orbitInfo = self.__dataProvider.OrbitInfo
            self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'WaveLength', orbitInfo.BandsWavelength[datasetname])
            bandstype = orbitInfo.BandsType[datasetname]
            if bandstype == 'REF':
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope',0.001)
        return


