from DataProvider import *
from HdfOperator import *
import numpy as N
from Parameters import *



class H8Dataprovider(DataProvider):
    __HdfOperator = HdfOperator()
    __latFileHandle = None
    __lonFileHandle = None
    __DataFileHandle = None
    __fileName = None
    __longitude = None
    __latitude = None
    __dataRes = 4000
    __dataWidthAndHeight= 2750
    __obsDataCount = 4


    __waveLenthlist = None

    def __init__(self):
        super(H8Dataprovider,self).__init__()

        return

    def __InitOrbitInfo(self):
        self.OrbitInfo.Sat = 'Himawari 8'
        self.OrbitInfo.Sensor = 'AHI'
        self.OrbitInfo.OrbitDirection= ''

        self.OrbitInfo.Width = self.__dataWidthAndHeight
        self.OrbitInfo.Height = self.__dataWidthAndHeight

        # solarzenith = self.GetSolarZenith()
        # if solarzenith[int(self.__dataWidthAndHeight/2),int(self.__dataWidthAndHeight/2)] <=85:
        #     self.OrbitInfo.DNFlag = 'D'
        # else:
        #     self.OrbitInfo.DNFlag = 'N'

        self.OrbitInfo.Date=''
        self.OrbitInfo.Time=''

        self.CreateBandsInfo()

    def SetFile(self,file):
        self.__latFileHandle = self.__HdfOperator.Open(file[0])
        self.__lonFileHandle = self.__HdfOperator.Open(file[1])
        self.__DataFileHandle = self.__HdfOperator.Open(file[2])
        self.__fileName = file[2]
        if '_2000M_' in self.__fileName:
            self.__dataRes = 2000
            self.__dataWidthAndHeight = 5500
            self.__obsDataCount = 16
            self.__waveLenthlist = ['0046', '0051', '0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
                                    '0860','0960','1040', '1120', '1230', '1330']
        elif '_0500M' in self.__fileName:
            self.__dataRes = 500
            self.__dataWidthAndHeight = 22000
            self.__obsDataCount = 1
            self.__waveLenthlist = ['0064']
        else:
            self.__waveLenthlist = ['0064', '0086', '0160', '0230', '0390', '0620', '0700', '0730',
                                    '0860', '0960', '1040', '1120', '1230', '1330']
            self.__obsDataCount = 14
        self.__InitOrbitInfo()


    def CreateBandsInfo(self):

        index  = 1
        for wavelength in self.__waveLenthlist:
            self.OrbitInfo.BandsWavelength['EVB'+str(index)] = wavelength
            if int(wavelength)>230:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'EMIS'
            else:
                self.OrbitInfo.BandsType['EVB'+str(index)] = 'REF'
            index = index+1


    def GetLongitude(self):

        return self.GetDataSet(self.__lonFileHandle, '/', 'Lon')


    def GetLatitude(self):

        return self.GetDataSet(self.__latFileHandle, '/', 'Lat')


    def GetResolution(self):
        return self.__dataRes

    def GetOBSData(self, band):

        bandname = self.__GetOBSDatasetName(band,self.__dataRes)
        ret = None
        if bandname!='':

            ret=self.GetDataSet(self.__DataFileHandle,'/', bandname)
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

    def GetSensorAzimuth(self):

        return self.GetDataSet(self.__DataFileHandle,'/','NOMSatelliteAzimuth')


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

    def GetSensorZenith(self):
        return self.GetDataSet(self.__DataFileHandle,'/','NOMSatelliteZenith')

    def GetSolarAzimuth(self):
        return self.GetDataSet(self.__DataFileHandle,'/','NOMSunAzimuth')

    def GetSolarZenith(self):
        return self.GetDataSet(self.__DataFileHandle,'/','NOMSunZenith')

    # def GetEmissData(self, band):
    #     return

    def GetFile(self):
        return  self.__fileName


