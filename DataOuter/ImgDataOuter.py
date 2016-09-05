from DataOuter import *
from HdfOperator import *
from DataProvider.DataProvider import *
import numpy as N
import gc
from PIL import Image


class ImgDataOuter(DataOuter):
    def __init__(self):
        super(ImgDataOuter, self).__init__()
        self.__HdfOperator = HdfOperator()

        self.__dataProvider = DataProvider()

        self.__flagimage = 1

        self.__colorTable = None

        self.__r = None
        self.__g = None
        self.__b = None

        self.__Height = 0
        self.__Width = 0

        # set color table
        z1 = [0, 30, 60, 120, 190, 255]
        z2 = [0, 110, 160, 210, 240, 255]

        self.__colorTable = N.zeros(65536)
        for i in range(0, 10000):
            a = (255.0 + 0.9999) * (i * 0.0001) / (1.11)
            for j in range(0, 5):
                if a >= z1[j] and a < z1[j + 1]:
                    b = (a - z1[j]) / (z1[j + 1] - z1[j])
                    self.__colorTable[i] = z2[j] + (z2[j + 1] - z2[j]) * b
                    j = 6
        return

    def Dispose(self):
        self.__dataProvider = None

    def trans(self, d):
        def transA(d):
            return self.__colorTable[d]

        transFunc = N.frompyfunc(transA, 1, 1)
        image = transFunc(d)

        return image

    def Save(self, projResult, dataProvider):
        self.__dataProvider = dataProvider

        para = self.getParameter()
        resolution = para.ProjectResolution

        dataDescription = self.__dataProvider.GetDataDescription()

        # savePath,saveFile =  os.path.split(savefile)
        # saveFile = saveFile.upper()
        # saveFile=saveFile.replace('.HDF','_Proj.HDF')

        saveFile = para.OutputPath + dataDescription + '_' + para.ProjectTaskName + '.HDF'

        if os.path.exists(saveFile):
            os.remove(saveFile)

        fileHandle = self.__HdfOperator.Open(saveFile)

        Evbcnt = dataProvider.GetOBSDataCount()
        if para.IsAuxiliaryFileMode == False:
            for i in xrange(1, Evbcnt + 1):
                self.WriteDataset('EVB' + str(i), projResult, fileHandle, resolution)
                self.WriteDatasetAttribute(fileHandle, 'EVB' + str(i))

        AuxiliaryDataNamesList = dataProvider.GetAuxiliaryDataNamesList()
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
        datatype = 0
        if 'EVB' in datasetname:
            data = (self.__dataProvider.GetOBSData(datasetname)).astype(N.int32)
        else:
            data = self.__dataProvider.GetAuxiliaryData(datasetname)
            if (data.dtype == N.float) | (data.dtype == N.float32) | (data.dtype == N.float64):
                data = data.astype(N.float32)
                datatype = 1
            else:
                data = data.astype(N.int32)

        if data is not None:
            savedata = projResult.CreateSaveData(data, resolution, datatype)
            if 'EVB' in datasetname:
                self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata.astype(N.uint16))
            else:
                self.__HdfOperator.WriteHdfDataset(fileHandle, '/', datasetname, savedata)

            para = self.getParameter()
            saveImage = para.OutputPath + para.ProjectTaskName + '.jpg'
            if 'EVB' in datasetname:
                if self.__flagimage == 1:
                    self.__r = self.trans(savedata)
                if self.__flagimage == 2:
                    self.__g = self.trans(savedata)
                if self.__flagimage == 3:
                    self.__b = self.trans(savedata)
                    self.__Height = savedata.shape[0]
                    self.__Width = savedata.shape[1]

                    rgbArray = N.zeros((int(self.__Height), int(self.__Width), 3), 'uint8')
                    rgbArray[:, :, 0] = self.__b
                    rgbArray[:, :, 1] = self.__g
                    rgbArray[:, :, 2] = self.__r
                    image = Image.fromarray(rgbArray)

                    image.save(saveImage)
                    # print 'Save '+ str(resolution)+'M'+ 'image'

            self.__flagimage = self.__flagimage + 1
            del data
            del savedata
            gc.collect()
            print 'Save ' + str(resolution) + 'M' + datasetname
        if self.__flagimage == 4:
            print 'Save ' + str(resolution) + 'M' + 'image'

    def WriteDatasetAttribute(self, fileHandle, datasetname):
        if 'EVB' in datasetname:
            orbitInfo = self.__dataProvider.OrbitInfo
            self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'WaveLength',
                                                        orbitInfo.BandsWavelength[datasetname])
            bandstype = orbitInfo.BandsType[datasetname]
            if bandstype == 'REF':
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope', 0.001)
            else:
                self.__HdfOperator.WriteHdfDatasetAttribute(fileHandle, '/', datasetname, 'slope', 0.01)
        return


