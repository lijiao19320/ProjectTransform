from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD

class FY3CVirrProvider(DataProvider):


    def __init__(self):
        super(FY3CVirrProvider,self).__init__()
        self.__HdfOperator = HdfOperator()

        self.__RefData = None
        self.__longitude = None
        self.__latitude = None
        self.__Width = '2048'
        self.__HdfFileHandleList = dict()
        self.__BandWaveLenthList = None
        self.__AuxiliaryDataNamesList = dict()
        self.__description = 'NULL'
        #self.__AuxiliaryDataNamesList.clear()
        #self.__HdfFileHandleList.clear()
        self.__obsDataCount = 0

        self.__reshapeBand = None
        self.__bandnumber = None
        self.__ret = None
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList

        # del self.__AuxiliaryDataNamesList

        for filehandle in self.__HdfFileHandleList:
            self.__HdfFileHandleList[filehandle].close()
        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(FY3CVirrProvider, self).Dispose()


    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = self.GetSat()
        self.OrbitInfo.Sensor = 'Visible and InfraRed Radiometer'
        self.OrbitInfo.OrbitDirection = self.GetOrbitDirection()
        self.OrbitInfo.DNFlag = self.GetDNFlag()
        self.OrbitInfo.Width = self.__Width
        self.OrbitInfo.Height = self.GetHeight()
        self.OrbitInfo.Date = self.GetDate()
        self.OrbitInfo.Time = self.GetTime()


    def GetSat(self):
        Sat = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Satellite Name')
        Sat_str = str(Sat)
        return Sat_str


    def GetOrbitDirection(self):
        OrbitDirection = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Orbit Direction')
        OrbitDirection_str = str(OrbitDirection)
        return OrbitDirection_str


    def GetDNFlag(self):
        DNFlag = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Day Or Night Flag')
        DNFlag_str = str(DNFlag)
        return DNFlag_str


    def GetHeight(self):
        Height = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Number Of Scans')
        Height_str = str(Height)
        return Height_str


    def GetDate(self):
        Date = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Data Creating Date')
        Date_str = str(Date)
        return Date_str


    def GetTime(self):
        Time = self.__HdfOperator.ReadHdfAttri(self.__HdfFileHandleList['L1'], '/', 'Data Creating Time')
        Time_str = str(Time)
        return Time_str


    def OnParametersUpdate(self):
        super(FY3CVirrProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount = len(self.__BandWaveLenthList)
        self.CreateBandsInfo()
        return


    def CreateBandsInfo(self):
        Index = 1
        for Index in range(1,11):
            self.OrbitInfo.BandsWavelength['EVB' + str(Index)] = self.__BandWaveLenthList[Index - 1]
            if (Index == 3 or Index == 4 or Index == 5):
                self.OrbitInfo.BandsType['EVB' + str(Index)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB' + str(Index)] = 'REF'
            Index=Index+1


    def SetLonLatFile(self,latfile,lonfile):
        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)


    def SetL1File(self,file):
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)
        self.__InitOrbitInfo()
        self.__description = self.OrbitInfo.Sat + '_' + self.OrbitInfo.Sensor + '_' + self.OrbitInfo.Date + '_' + self.OrbitInfo.Time


    def GetLongitude(self):
        return self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'Geolocation', 'Longitude')


    def GetLatitude(self):
        return self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'Geolocation', 'Latitude')


    def __GetOBSDatasetName(self, band):
        bandname = ''
        if band == 'EVB1':
            bandname = '0'
        elif band == 'EVB2':
            bandname = '1'
        elif band == 'EVB6':
            bandname = '2'
        elif band == 'EVB7':
            bandname = '3'
        elif band == 'EVB8':
            bandname = '4'
        elif band == 'EVB9':
            bandname = '5'
        elif band == 'EVB10':
            bandname = '6'

        elif band == 'EVB3':
            bandname = '0'
        elif band == 'EVB4':
            bandname = '1'
        elif band == 'EVB5':
            bandname = '2'

        return bandname


    def GetDataSet(self, filehandle, group, ds):

        data = self.__HdfOperator.ReadHdfDataset(filehandle, group, ds)

        startLine = self.startLine
        endlLine = self.endLine
        #ret0 = None

        if ds=='EV_RefSB' or ds=='EV_Emissive':
            if startLine != -1 & endlLine != -1:
                self.__ret = data[self.__bandnumber,startLine:endlLine, :]
            else:
                self.__ret = data[self.__bandnumber,:, :]
            return self.__ret
        else:

            if startLine != -1 & endlLine != -1:
                self.__ret = data[startLine:endlLine, :]
            else:
                self.__ret = data[:, :]
            return self.__ret


    def GetOBSData(self, band):
        self.__bandnumber = int(self.__GetOBSDatasetName(band))
        bandRef=['EVB1','EVB2','EVB6','EVB7','EVB8','EVB9','EVB10']

        if self.__RefData == None:
            if band in bandRef:
                self.__RefData = self.GetDataSet(self.__HdfFileHandleList['L1'], 'Data', 'EV_RefSB')
            else:
                self.__RefData = self.GetDataSet(self.__HdfFileHandleList['L1'], 'Data', 'EV_Emissive')

            self.__reshapeBand=self.__RefData
            self.__RefData=None
            return self.__reshapeBand


    def GetOBSDataCount(self):
        return 10

    def GetResolution(self):
        return 1000

    # def SetParameter(self, papameter):
    #
    #     return
    def SetInputString(self,value):
        self.InputString = value

    def GetInputString(self):
        return  self.InputString

    def SetAuxiliaryDataFile(self, LNDfile, LMKfile, DEMfile, COASTfile, SATZENfile, SATAZIfile, Lonfile, LatFile):

        if LNDfile != 'NULL':
            self.__HdfFileHandleList['LandCover'] = self.__HdfOperator.Open(LNDfile)
            self.__AuxiliaryDataNamesList['LandCover'] = 'LandCover'
        if LMKfile != 'NULL':
            self.__HdfFileHandleList['LandSeaMask'] = self.__HdfOperator.Open(LMKfile)
            self.__AuxiliaryDataNamesList['LandSeaMask'] = 'LandSeaMask'
        if DEMfile != 'NULL':
            self.__HdfFileHandleList['DEM'] = self.__HdfOperator.Open(DEMfile)
            self.__AuxiliaryDataNamesList['DEM'] = 'DEM'
        if COASTfile != 'NULL':
            self.__HdfFileHandleList['SeaCoast'] = self.__HdfOperator.Open(COASTfile)
            self.__AuxiliaryDataNamesList['SeaCoast'] = 'SeaCoast'
            #self.__AuxiliaryDataNamesList['SeaCoast'] = 'NULL'
        if SATZENfile != 'NULL':
            self.__HdfFileHandleList['SensorZenith'] = self.__HdfOperator.Open(SATZENfile)
            self.__AuxiliaryDataNamesList['SensorZenith'] = 'SensorZenith'
        if SATAZIfile != 'NULL':
            self.__HdfFileHandleList['SensorAzimuth'] = self.__HdfOperator.Open(SATAZIfile)
            self.__AuxiliaryDataNamesList['SensorAzimuth'] = 'SensorAzimuth'
        if Lonfile != 'NULL':
            self.__AuxiliaryDataNamesList['Longitude'] = 'Longitude'
        if LatFile != 'NULL':
            self.__AuxiliaryDataNamesList['Latitude'] = 'Latitude'

        return
    def GetAuxiliaryData(self,dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname =='':
            return  ret

        ret=self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'Geolocation', dsname)

        return ret


    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription() + '_' + str(
                self.GetParameter().ProjectResolution)
        return self.__description