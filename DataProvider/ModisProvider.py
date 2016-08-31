from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
from natsort import natsorted, ns


class ModisProvider(DataProvider):

    def __init__(self):
        super(ModisProvider, self).__init__()
        self.__AuxiliaryDataNamesList = dict()
        self.__HdfFileHandleList = dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataHeight = 0
        self.__dataWidth = 0
        self.__band = 0
        self.__refbandname = None
        self.__emisbandname = None

        return


    # __dataRes = 1000
    # __dataHeight = 3660
    # __dataWidth = 1354
    # __obsDataCount = 31
    # __band = 0
    # __waveLenthlist = None


    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList = None

        # del self.__AuxiliaryDataNamesList
        for filehandle in self.__HdfFileHandleList:
            self.__HdfFileHandleList[filehandle].end()

        self.__HdfFileHandleList.clear()

        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(ModisProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Modis'
        self.OrbitInfo.OrbitDirection = ''

        self.OrbitInfo.Width = self.__dataWidth
        self.OrbitInfo.Height = self.__dataHeight

        self.OrbitInfo.Date = ''
        self.OrbitInfo.Time = ''

    def OnParametersUpdate(self):
        super(ModisProvider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount = len(self.__BandWaveLenthList)
        self.CreateBandsInfo()

        return

        # self.__waveLenthlist = ['405', '438', '483', '526', '546', '662', '672', '673', '683', '743',
        #                         '862', '890', '931', '915', '3660', '3929', '3930', '4020', '4433', '4482',
        #                         '1360', '6535', '7175', '8400', '9580', '10780', '11770', '13185', '13485', '13785',
        #                         '18085']
        #
        # self.CreateBandsInfo()

    def SetLonLatFile(self, latfile, lonfile):

        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)

    def SetL1File(self, file):
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)
        # hdf = SD(FILE_NAME, SDC.READ)

        if 'AQUA' in file:
            self.OrbitInfo.Sensor = 'AQUA'
            if '1KM' in file:
                self.__dataRes = 1000
                self.__dataWidth = 1354
                self.__dataHeight = 3660
                # self.__obsDataCount = 16
                # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
                #                         '0860','0960','1040', '1120', '1230', '1330']
            elif 'HKM' in file:
                self.__dataRes = 500
                self.__dataWidth = 2708
                self.__dataHeight = 7320
                # self.__obsDataCount = 1
                # self.__BandWaveLenthList = ['0064']
            else:
                self.__dataRes = 250
                self.__dataWidth = 5416
                self.__dataHeight = 14640

        else:
            self.OrbitInfo.Sensor = 'TERRA'
            if '1KM' in file:
                self.__dataRes = 1000
                self.__dataWidth = 1354
                self.__dataHeight = 3660
                # self.__obsDataCount = 16
                # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
                #                         '0860','0960','1040', '1120', '1230', '1330']
            elif 'HKM' in file:
                self.__dataRes = 500
                self.__dataWidth = 2708
                self.__dataHeight = 7320
                # self.__obsDataCount = 1
                # self.__BandWaveLenthList = ['0064']
            else:
                self.__dataRes = 250
                self.__dataWidth = 5416
                self.__dataHeight = 14640





            # self.__obsDataCount = 4
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086']
        # else:
        #     self.__BandWaveLenthList = ['0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
        #                             '0860', '0960', '1040', '1120', '1230', '1330']
        #     self.__obsDataCount = 14

        # path, filename = os.path.split(file)
        # self.__description = filename.upper().replace('.HDF', '')
        self.__InitOrbitInfo()
        self.__description = self.OrbitInfo.Sat + '_' + self.OrbitInfo.Sensor + '_' + self.OrbitInfo.Date + '_' + self.OrbitInfo.Time

    # def SetL1File(self, file):
    #
    #     # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
    #     self.__filehandel = self.__HdfOperator.Open(file)
    #     self.__fileName = file
    #     self.__InitOrbitInfo()

    def SetAuxiliaryDataFile(self, LNDfile, LMKfile, DEMfile, COASTfile, SATZENfile, SATAZIfile, Lonfile, Latfile):

        if LNDfile!='NULL':
            self.__HdfFileHandleList['LandCover'] = self.__HdfOperator.Open(LNDfile)
            self.__AuxiliaryDataNamesList['LandCover'] = 'LandCover'
        if LMKfile!='NULL':
            self.__HdfFileHandleList['Land/SeaMask'] = self.__HdfOperator.Open(LMKfile)
            self.__AuxiliaryDataNamesList['Land/SeaMask'] = 'Land/SeaMask'
        if DEMfile!='NULL':
            self.__HdfFileHandleList['DEM'] = self.__HdfOperator.Open(DEMfile)
            self.__AuxiliaryDataNamesList['DEM'] = 'DEM'
        if COASTfile!='NULL':
            self.__HdfFileHandleList['SeaCoast']= self.__HdfOperator.Open(COASTfile)
            self.__AuxiliaryDataNamesList['SeaCoast'] = 'SeaCoast'
        if SATZENfile!='NULL':
            self.__HdfFileHandleList['SensorZenith']= self.__HdfOperator.Open(SATZENfile)
            self.__AuxiliaryDataNamesList['SensorZenith'] = 'SensorZenith'
        if SATAZIfile!='NULL':
            self.__HdfFileHandleList['SensorAzimuth']= self.__HdfOperator.Open(SATAZIfile)
            self.__AuxiliaryDataNamesList['SensorAzimuth'] = 'SensorAzimuth'
        if Lonfile != 'NULL':
            self.__AuxiliaryDataNamesList['Longitude'] = 'Longitude'
        if Latfile != 'NULL':
            self.__AuxiliaryDataNamesList['Latitude'] = 'Latitude'

        return


    def CreateBandsInfo(self):

        index = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(index)] = wavelength
            if int(wavelength) < 2135:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'REF'
            else:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'EMIS'
            index = index+1




    def GetLongitude(self):

        return self.GetDataSet('Longitude')

    def GetLatitude(self):

        return self.GetDataSet('Latitude')


    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):
        self.__band = band

        (self.__refbandname, self.__emisbandname) = self.__GetOBSDatasetName(band)

        ret = None
        if band in self.__refbandname:
            ret=self.GetDataSet(band)
        else:
            ret = self.GetDataSet(band)

        return ret

    def __GetOBSDatasetName(self, band):
        self.refBand = dict()
        self.emisBand = dict()
        self.refBandname = dict()
        self.emisBandname = dict()

        for band in self.OrbitInfo.BandsType:
            if self.OrbitInfo.BandsType[band] == 'REF':
                self.refBand[band] = self.OrbitInfo.BandsType[band]
            else:
                self.emisBand[band] = self.OrbitInfo.BandsType[band]

        self.refBand = natsorted(self.refBand, alg=ns.IGNORECASE)
        self.emisBand = natsorted(self.emisBand, alg=ns.IGNORECASE)

        refNum = 0
        for refband in self.refBand:
            self.refBandname[refband] = refNum
            refNum = refNum + 1

        emisNum = 0
        for emisband in self.emisBand:
            self.emisBandname[emisband] = emisNum
            emisNum = emisNum + 1

        return self.refBandname, self.emisBandname


    def GetOBSDataCount(self):
        return self.__obsDataCount


    def GetDataSet(self,band):

        startLine = self.startLine
        endlLine = self.endLine
        ret = None

        (self.__refbandname, self.__emisbandname) = self.__GetOBSDatasetName(band)


        if band in self.__refbandname:
            data = self.__HdfFileHandleList['L1'].select('EV_1KM_RefSB')
            if startLine != -1 and endlLine != -1:
                ret = data[self.__refbandname[self.__band], startLine:endlLine, :]
            else:
                ret = data[self.__refbandname[self.__band], :, :]
        elif band in self.__emisbandname:
            data = self.__HdfFileHandleList['L1'].select('EV_1KM_Emissive')
            if startLine != -1 and endlLine != -1:
                ret = data[self.__emisbandname[self.__band], startLine:endlLine, :]
            else:
                ret = data[self.__emisbandname[self.__band], :, :]

        else:
            data = self.__HdfFileHandleList[band].select(band)
            if startLine != -1 & endlLine != -1:
                ret = data[startLine:endlLine, :]
            else:
                ret = data[:, :]

        return ret

    def GetAuxiliaryData(self, dataname):

        dsname = self.__AuxiliaryDataNamesList[dataname]
        ret = None
        if dsname == '':
            return ret

        ret = self.GetDataSet(dsname)

        return ret

    def GetAuxiliaryDataNamesList(self):
        return self.__AuxiliaryDataNamesList
    #
    # def GetSensorZenith(self):
    #     return self.GetDataSet(self.__DataFileHandle,'/','NOMSatelliteZenith')
    #
    # def GetSolarAzimuth(self):
    #     return self.GetDataSet(self.__DataFileHandle,'/','NOMSunAzimuth')
    #
    # def GetSolarZenith(self):
    #     return self.GetDataSet(self.__DataFileHandle,'/','NOMSunZenith')

    # def GetEmissData(self, band):
    #     return

    # def SetInputString(self,value):
    #     self.InputString = value
    #
    # def GetInputString(self):
    #     return  self.InputString
    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription() + '_' + str(
                self.GetParameter().ProjectResolution)
        return self.__description


