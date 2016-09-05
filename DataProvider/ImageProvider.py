from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *



class ImageProvider(DataProvider):
    def __init__(self):
        super(ImageProvider, self).__init__()
        self.__AuxiliaryDataNamesList = dict()
        self.__HdfFileHandleList = dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidthAndHeight = 0

        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList = None

        # del self.__AuxiliaryDataNamesList
        for filehandle in self.__HdfFileHandleList:
            if filehandle != 'L1':
                self.__HdfFileHandleList[filehandle].close()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(ImageProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Himawari 8'
        self.OrbitInfo.Sensor = 'AHI'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        self.OrbitInfo.Date=''
        self.OrbitInfo.Time=''

        self.CreateBandsInfo()

    def OnParametersUpdate(self):
        super(ImageProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount = len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

    def SetLonLatFile(self,latfile,lonfile):

        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)


    def SetL1File(self, file):

        self.__HdfFileHandleList['L1'] = file


        if '_1000M_' in file:
            self.__dataRes = 1000
            self.__dataWidthAndHeight = 11000
            self.__obsDataCount = 3
            self.__BandWaveLenthList = ['0046', '0051', '0064']
        self.__InitOrbitInfo()
        self.__description = self.OrbitInfo.Sat + '_' + self.OrbitInfo.Sensor + '_' + self.OrbitInfo.Date + '_' + self.OrbitInfo.Time

    def SetAuxiliaryDataFile(self,LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Lonfile,LatFile):

        if LNDfile!='NULL':
            self.__HdfFileHandleList['LandCover'] = self.__HdfOperator.Open(LNDfile)
            self.__AuxiliaryDataNamesList['LandCover'] = 'LandCover'
        if LMKfile!='NULL':
            self.__HdfFileHandleList['LandSeaMask'] = self.__HdfOperator.Open(LMKfile)
            self.__AuxiliaryDataNamesList['LandSeaMask'] = 'LandSeaMask'
        if DEMfile!='NULL':
            self.__HdfFileHandleList['DEM'] = self.__HdfOperator.Open(DEMfile)
            self.__AuxiliaryDataNamesList['DEM'] = 'DEM'
        if COASTfile!='NULL':
            self.__HdfFileHandleList['SeaCoast']= self.__HdfOperator.Open(COASTfile)
            self.__AuxiliaryDataNamesList['SeaCoast'] = 'SeaCoast'
        if SATZENfile!='NULL':
            self.__HdfFileHandleList['SensorZenith']= self.__HdfOperator.Open(SATZENfile)
            self.__AuxiliaryDataNamesList['SensorZenith'] = 'SatZenith'
        if SATAZIfile!='NULL':
            self.__HdfFileHandleList['SensorAzimuth']= self.__HdfOperator.Open(SATAZIfile)
            self.__AuxiliaryDataNamesList['SensorAzimuth'] = 'SatAzimuth'
        if Lonfile != 'NULL':
            self.__AuxiliaryDataNamesList['Longitude'] = 'Lon'
        if LatFile != 'NULL':
            self.__AuxiliaryDataNamesList['Latitude'] = 'Lat'

        return


    def CreateBandsInfo(self):

        index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(index)] = wavelength
            if int(wavelength)>230:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'REF'
            index = index+1


    def GetLongitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Longitude'], '/', 'Lon')


    def GetLatitude(self):

        return self.GetDataSet(self.__HdfFileHandleList['Latitude'], '/', 'Lat')


    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        ret = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', band)

        return ret

    def GetOBSDataCount(self):
        return self.__obsDataCount

    def GetDataSet(self,filehandle,group,ds):

        data = None

        if 'EVB' in ds:
            Filename = str(filehandle)
            if ds == 'EVB1':
                B = Filename
                with open(B, 'rb') as f:
                    data = N.fromfile(f, dtype=N.float32)
                    data = N.reshape(data, [self.__dataWidthAndHeight, self.__dataWidthAndHeight])

            elif ds == 'EVB2':
                B = Filename.replace('B1', 'B2')
                with open(B, 'rb') as f:
                    data = N.fromfile(f, dtype=N.float32)
                    data = N.reshape(data, [self.__dataWidthAndHeight, self.__dataWidthAndHeight])
            elif ds == 'EVB3':
                B = Filename.replace('B1', 'B3')
                with open(B, 'rb') as f:
                    data = N.fromfile(f, dtype=N.float32)
                    data = N.reshape(data, [self.__dataWidthAndHeight, self.__dataWidthAndHeight])
        else:
            data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)

        startLine = self.startLine
        endlLine = self.endLine
        ret = None
        if startLine!= -1 & endlLine!= -1:
            ret = data[startLine:endlLine, :]
        else:
            ret = data[:,:]
        return ret

    def GetAuxiliaryData(self,dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname =='':
            return  ret

        ret=self.GetDataSet(self.__HdfFileHandleList[dataname], '/', dsname)

        return ret


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription() + '_' + str(
                self.GetParameter().ProjectResolution)
        return self.__description



