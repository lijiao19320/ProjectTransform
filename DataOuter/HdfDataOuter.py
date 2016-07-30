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

        inputString = self.__dataProvider.GetInputString()

        # savePath,saveFile =  os.path.split(savefile)
        # saveFile = saveFile.upper()
        # saveFile=saveFile.replace('.HDF','_Proj.HDF')
        if inputString!='NULL':
            saveFile = para.OutputPath+inputString+'_Proj.HDF'
        else:
            saveFile = para.OutputPath+'static.HDF'

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


        # elif datasetname == 'SensorAzimuth':
        #     data = (self.__dataProvider.GetSensorAzimuth()).astype(N.float32)
        #     datatype=1
        # elif datasetname == 'SensorZenith':
        #     data = (self.__dataProvider.GetSensorZenith()).astype(N.float32)
        #     datatype=1
        # elif datasetname == 'SolarAzimuth':
        #     data = (self.__dataProvider.GetSolarAzimuth()).astype(N.float32)
        #     datatype=1
        # elif datasetname == 'SolarZenith':
        #     data = (self.__dataProvider.GetSolarZenith()).astype(N.float32)
        #     datatype=1

        # U = projResult.U
        # V = projResult.V
        if data != None:
            savedata = projResult.CreateSaveData(data,resolution,datatype)
            self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata)

            print 'Save '+datasetname

    def WriteDatasetAttribute(self,fileHandle,datasetname):
        if 'EVB' in datasetname:
            orbitInfo = self.__dataProvider.OrbitInfo
            self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'WaveLength', orbitInfo.BandsWavelength[datasetname])
            bandstype = orbitInfo.BandsType[datasetname]
            if bandstype == 'REF':
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope',0.001)
        return


