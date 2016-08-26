from DataProvider import *
from HdfOperator import *
import types
import numpy as N
from Parameters import *
import ProjOutputData_module as SD


class NPPProvider(DataProvider):


    def __init__(self):
        super(NPPProvider,self).__init__()
        self.__AuxiliaryDataNamesList =dict()
        self.__HdfFileHandleList =dict()
        self.__obsDataCount = 0
        self.__description = 'NULL'
        self.__BandWaveLenthList = None

        self.__HdfOperator = HdfOperator()

        self.__longitude = None
        self.__latitude = None
        self.__dataRes = 0
        self.__dataWidth = 0
        self.__dataHeight = 0
        self.__filenamelist=''
        ##file_index = 0
        return

    def Dispose(self):
        self.__AuxiliaryDataNamesList.clear()
        if self.__BandWaveLenthList is not None:
            del self.__BandWaveLenthList
            self.__BandWaveLenthList=None
        # del self.__AuxiliaryDataNamesList
        for filehandle in self.__HdfFileHandleList:
            self.__HdfFileHandleList[filehandle].close()

        self.__HdfFileHandleList.clear()
        self.__description = 'NULL'
        self.__obsDataCount = 0
        super(NPPProvider, self).Dispose()

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'NPP'
        self.OrbitInfo.Sensor = 'VIIRS'
        ##self.OrbitInfo.OrbitDirection= ''
        self.OrbitInfo.Width = self.__dataWidth
        self.OrbitInfo.Height = self.__dataHeight

        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date=self.GetDate()
        self.OrbitInfo.Time=self.GetTime()

    def GetDate(self):
        filehandle=self.__HdfFileHandleList['L1_1']
        Date = self.__HdfOperator.ReadHdfAttri(filehandle,'/','N_HDF_Creation_Date')
        return Date

    def GetTime(self):
        filehandle = self.__HdfFileHandleList['L1_1']
        Time = self.__HdfOperator.ReadHdfAttri(filehandle, '/', 'N_HDF_Creation_Time')
        return Time

    def OnParametersUpdate(self):
        super(NPPProvider, self).OnParametersUpdate()
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
        # filepath = os.path.split(file)
        # filename = filepath[1]
        self.__filenamelist = file
        if '_svi' in file:
            self.__dataRes = 350
            self.__dataWidth = 6400
            self.__dataHeight = 10752
            for index in range(1,6):
                file_each = self.__filenamelist.replace('svi01','svi0'+str(index))
                self.__HdfFileHandleList['L1_'+str(index)] = self.__HdfOperator.Open(file_each)
        elif '_svm' in file:
            self.__dataRes = 750
            self.__dataWidth = 3200
            self.__dataHeight = 5376
            for index2 in range(1, 17):
                if index2 <10:
                    file_each = self.__filenamelist.replace('svm01','svm0'+str(index2))
                    self.__HdfFileHandleList['L1_' + str(index2)] = self.__HdfOperator.Open(file_each)
                else:
                    file_each = self.__filenamelist.replace('svm01','svm'+str(index2))
                    self.__HdfFileHandleList['L1_' + str(index2)] = self.__HdfOperator.Open(file_each)
        else:
            self.__dataRes = 750
            self.__dataWidth = 4064
            self.__dataHeight = 5376
            self.__HdfFileHandleList['L1_1'] = self.__HdfOperator.Open(self.__filenamelist)
                # self.__obsDataCount = 1
            # self.__BandWaveLenthList = ['0064']
        # elif '_svdnb' in file:
        #     self.__HdfFileHandleList['L1_1'] = self.__HdfOperator.Open(file)
        #     self.__dataRes = 800
        #     self.__dataWidth = 4063
        #     self.__dataHeight = 5375
            # self.__obsDataCount = 4
            # self.__BandWaveLenthList = ['0046', '0051', '0064', '0086']
        # else:
        #     self.__BandWaveLenthList = ['0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
        #                             '0860', '0960', '1040', '1120', '1230', '1330']
        #     self.__obsDataCount = 14

        # path, filename = os.path.split(file)
        # self.__description = filename.upper().replace('.HDF', '')
        self.__InitOrbitInfo()
        self.__description=self.OrbitInfo.Sat+'_'+self.OrbitInfo.Sensor###+'_'+self.OrbitInfo.Date+'_'+self.OrbitInfo.Time


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
            self.__AuxiliaryDataNamesList['SensorZenith'] = 'SatelliteZenithAngle'
        if SATAZIfile!='NULL':
            self.__HdfFileHandleList['SensorAzimuth']= self.__HdfOperator.Open(SATAZIfile)
            self.__AuxiliaryDataNamesList['SensorAzimuth'] = 'SatelliteAzimuthAngle'
        if Lonfile != 'NULL':
            self.__AuxiliaryDataNamesList['Longitude'] = 'Longitude'
        if LatFile != 'NULL':
            self.__AuxiliaryDataNamesList['Latitude'] = 'Latitude'

        return


    def CreateBandsInfo(self):

        index  = 1
        for wavelength in self.__BandWaveLenthList:
            self.OrbitInfo.BandsWavelength['EVB'+str(index)] = wavelength

            if '_svi' in self.__filenamelist:

                self.OrbitInfo.BandsType['EVB1'] = 'REF'
                self.OrbitInfo.BandsType['EVB2'] = 'REF'
                self.OrbitInfo.BandsType['EVB3'] = 'REF'
                # self.OrbitInfo.BandsType['EVB4'] = 'KELVINS'
                # self.OrbitInfo.BandsType['EVB5'] = 'KELVINS'
                self.OrbitInfo.BandsType['EVB4'] = 'EMIS'
                self.OrbitInfo.BandsType['EVB5'] = 'EMIS'
            elif '_svm' in self.__filenamelist:
                if index<=11:
                    self.OrbitInfo.BandsType['EVB' + str(index)] = 'REF'
                else:
                    self.OrbitInfo.BandsType['EVB' + str(index)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB' + str(index)] = 'EMIS'
            index = index+1


    def GetLongitude(self):
        HdfFileHandleList_str = str(self.__HdfFileHandleList['Longitude'])
        if '_gitco' in HdfFileHandleList_str:
            return self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'All_Data','VIIRS-IMG-GEO-TC_All/Longitude')
        elif '_gmtco' in HdfFileHandleList_str:
            return self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'All_Data','VIIRS-MOD-GEO-TC_All/Longitude')
        else:
            return self.GetDataSet(self.__HdfFileHandleList['Longitude'], 'All_Data', 'VIIRS-DNB-GEO_All/Longitude')

    def GetLatitude(self):
        HdfFileHandleList_str = str(self.__HdfFileHandleList['Latitude'])
        if '_gitco' in HdfFileHandleList_str:
            return self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'All_Data', 'VIIRS-IMG-GEO-TC_All/Latitude')
        elif '_gmtco' in HdfFileHandleList_str:
            return self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'All_Data','VIIRS-MOD-GEO-TC_All/Latitude')
        else:
            return self.GetDataSet(self.__HdfFileHandleList['Latitude'], 'All_Data', 'VIIRS-DNB-GEO_All/Latitude')

    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):
        ret = None
        if '_svi' in self.__filenamelist:
                index = int(band[3:])
                groupname = 'VIIRS-I' + str(index) + '-SDR_All'
                each_file = self.__HdfFileHandleList['L1_'+str(index)]
                if index <=3:
                    ret = self.GetDataSet(each_file, 'All_Data',groupname + '/Reflectance')[:, :].astype(N.int32)
                else:
                    ret = self.GetDataSet(each_file, 'All_Data', groupname + '/Radiance')[:, :].astype(N.int32)
        elif '_svm' in self.__filenamelist:
                index = int(band[3:])
                groupname = 'VIIRS-M' + str(index) + '-SDR_All'
                each_file = self.__HdfFileHandleList['L1_' + str(index)]

                if index<= 11:
                    ret = self.GetDataSet(each_file, 'All_Data',groupname+'/Reflectance')[:, :].astype(N.int32)
                else:
                    ret = self.GetDataSet(each_file, 'All_Data', groupname + '/Radiance')[:, :].astype(N.int32)
        else:
                index = int(band[3:])
                each_file = self.__HdfFileHandleList['L1_' + str(index)]
                ret = self.GetDataSet(each_file, 'All_Data', 'VIIRS-DNB-SDR_All/Radiance')[:, :].astype(N.int32)


        # caltable = self.GetDataSet(self.__HdfFileHandleList['L1'], '/', caltableName)
            #caltable = self.__HdfOperator.ReadHdfDataset(self.__HdfFileHandleList['L1'], '/', caltableName)[:].astype(N.float32)

        return ret
    #
    # def __GetOBSDatasetName(self, band,datares):
    #     bandname = ''
    #     waveLength = self.OrbitInfo.BandsWavelength[band]
    #     if self.OrbitInfo.BandsType[band] == 'REF':
    #         bandname = 'NOMChannelVIS'+waveLength+'_'+str(datares)
    #     else:
    #         bandname = 'NOMChannelIRX' + waveLength + '_'+str(datares)
    #
    #     return  bandname


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
        HdfFileHandleList_str = str(self.__HdfFileHandleList[dataname])
        if '_gitco' in HdfFileHandleList_str:
            ret = self.GetDataSet(self.__HdfFileHandleList[dataname], 'All_Data','VIIRS-IMG-GEO-TC_All/'+dsname)
        elif '_gmtco' in HdfFileHandleList_str:

            ret = self.GetDataSet(self.__HdfFileHandleList[dataname], 'All_Data','VIIRS-MOD-GEO-TC_All/'+ dsname)
        else:

            ret = self.GetDataSet(self.__HdfFileHandleList[dataname], 'All_Data','VIIRS-DNB-GEO_All/' + dsname)

        return ret

    def GetOBSDataCount(self):
        return self.__obsDataCount


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


