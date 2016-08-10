from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *



class H8Dataprovider(DataProvider):
    __HdfOperator = HdfOperator()


    __HdfFileHandleList = dict()


    __longitude = None
    __latitude = None
    __dataRes = 4000
    __dataWidthAndHeight= 2750
    __obsDataCount = 0


    __BandWaveLenthList = None

    __AuxiliaryDataNamesList = dict()

    __description = 'NULL'

    def __init__(self):
        super(H8Dataprovider,self).__init__()
        self.__AuxiliaryDataNamesList.clear()
        self.__HdfFileHandleList.clear()

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

        super(H8Dataprovider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Himawari8'
        self.OrbitInfo.Sensor = 'OBI'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date=self.GetDate()
        self.OrbitInfo.Time=self.GetTime()




    def GetDate(self):
        filehandle=self.__HdfFileHandleList['L1']

        year = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartYear')
        month = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartMonth')
        day = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartDay')
        strmonth = '{:0>2}'.format(str(month[0]))
        srtday = '{:0>2}'.format(str(day[0]))
        stryear = '{:0>4}'.format(str(year[0]))
        return stryear+strmonth+srtday

    def GetTime(self):
        filehandle=self.__HdfFileHandleList['L1']

        hour = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartHour')
        minute = self.__HdfOperator.ReadHdfAttri(filehandle,'/','iStartMinute')

        strhour= '{:0>2}'.format(str(hour[0]))
        srtminute = '{:0>2}'.format(str(minute[0]))

        return strhour+srtminute

    def OnParametersUpdate(self):
        super(H8Dataprovider, self).OnParametersUpdate()

        self.__BandWaveLenthList = self.GetParameter().BandWaveLengthList

        self.__obsDataCount =len(self.__BandWaveLenthList)
        self.CreateBandsInfo()
        return

    def SetLonLatFile(self,latfile,lonfile):
        # self.__latFileHandle = self.__HdfOperator.Open(latfile)
        # self.__lonFileHandle = self.__HdfOperator.Open(lonfile)l
        self.__HdfFileHandleList['Latitude'] = self.__HdfOperator.Open(latfile)
        self.__HdfFileHandleList['Longitude'] = self.__HdfOperator.Open(lonfile)

    def SetL1File(self, file):

        # self.__L1DataFileHandle = self.__HdfOperator.Open(file)
        self.__HdfFileHandleList['L1'] = self.__HdfOperator.Open(file)

        if '_2000M_' in file:
            self.__dataRes = 2000
            self.__dataWidthAndHeight = 5500
            # self.__obsDataCount = 16
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
            #                         '0860','0960','1040', '1120', '1230', '1330']
        elif '_0500M' in file:
            self.__dataRes = 500
            self.__dataWidthAndHeight = 22000
            # self.__obsDataCount = 1
            # self.__BandWaveLenthList = ['0064']
        elif '_1000M' in file:
            self.__dataRes = 1000
            self.__dataWidthAndHeight = 11000
            # self.__obsDataCount = 4
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086']
        # else:
        #     self.__BandWaveLenthList = ['0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
        #                             '0860', '0960', '1040', '1120', '1230', '1330']
        #     self.__obsDataCount = 14

        # path, filename = os.path.split(file)
        # self.__description = filename.upper().replace('.HDF', '')
        self.__InitOrbitInfo()
        self.__description=self.OrbitInfo.Sat+'_'+self.OrbitInfo.Sensor+'_'+self.OrbitInfo.Date+'_'+self.OrbitInfo.Time


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

        bandname = self.__GetOBSDatasetName(band,self.__dataRes)
        ret = None
        if bandname!='':

            ret=self.GetDataSet(self.__HdfFileHandleList['L1'], '/', bandname)
            # caltable = self.

        return ret

    def __GetOBSDatasetName(self, band,datares):
        bandname = ''
        waveLength = self.OrbitInfo.BandsWavelength[band]
        if self.OrbitInfo.BandsType[band] == 'REF':
            bandname = 'NOMChannelVIS'+waveLength+'_'+str(datares)
        else:
            bandname = 'NOMChannelIRX' + waveLength + '_'+str(datares)

        return  bandname

    def GetOBSDataCount(self):
        return self.__obsDataCount

    # def GetSensorAzimuth(self):
    #
    #     return self.GetDataSet(self.__DataFileHandle,'/','NOMSatelliteAzimuth')


    def GetDataSet(self,filehandle,group,ds):

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

    # def SetDataDescription(self, value):
    #     self.__description = value

    def GetDataDescription(self):
        if self.__description == 'NULL':
            self.__description = self.GetParameter().GetParamDescription()+'_'+str(self.GetParameter().ProjectResolution)
        return  self.__description


