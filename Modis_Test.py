from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from DataProvider.ModisProvider import *
from ProjProcessor import *
from ParameterParser import *

import multiprocessing


L1FilePath = ''
def ProviderFactory(isCreateAuxfile,resolution):
    provider = None
    if isCreateAuxfile:
        provider = CreateAuxilaryProvider(resolution)
    else:
        provider = CreateStdProjProvider(resolution)

    return provider


def CreateAuxilaryProvider(resolution):
    provider = ModisProvider()

    Latfile='/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'
    Lonfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'

    # if resolution == 1000:
    #     Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf'
    #     Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf'
    # elif resolution ==500:
    #     Latfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LAT.HDF'
    #     Lonfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LON.HDF'
    #
    LNDfile = 'NULL'
    LMKfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'
    DEMfile = 'NULL'
    COASTfile = 'NULL'
    # SATZENfile = 'NULL'
    # SATAZIfile = 'NULL'
    SATZENfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'
    SATAZIfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(LNDfile, LMKfile, DEMfile, COASTfile, SATZENfile, SATAZIfile, Lonfile, Latfile)
    # provider.SetInputString(param.GetParamID())
    return  provider

def CreateStdProjProvider(resolution):
    provider = ModisProvider()

    Latfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'
    Lonfile = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD03.hdf'
    L1file = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD021KM.hdf'

    # if resolution == 1000:
    #     Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf'
    #     Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf'
    #     L1file = L1FilePath+'AHI8_OBI_1000M_NOM_' + sys.argv[1] + '.hdf'
    #
    # elif resolution == 500:
    #     Latfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LAT.HDF'
    #     Lonfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LON.HDF'
    #     L1file = L1FilePath+'AHI8_OBI_0500M_NOM_' + sys.argv[1] + '.hdf'


    provider.SetLonLatFile(Latfile,
                           Lonfile)

    # print sys.argv[1]
    provider.SetL1File(L1file)

    # provider.SetInputString(InputString)
    return  provider

def ProcessProj(param,reslution,isCreateAuxfile):

    provider = ProviderFactory(isCreateAuxfile,reslution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML('/home/lijiao/Documents/Modis/H8_1000m_Proj.xml')
    auxparam.OutputPath = '/home/lijiao/Documents/Modis/output/'
    auxparam.IsAuxiliaryFileMode = True
    auxparam.ProjectResolution = resolution
    ProcessProj(auxparam, resolution, True)


if __name__ == '__main__':

    L1FilePath = '/home/lijiao/Documents/Modis/h4/AQUA_X_2015_10_15_12_58_A_G.MOD021KM.hdf'
    paramparser = ParameterParser()
    param = paramparser.parseXML('/home/lijiao/Documents/Modis/H8_1000m_Proj.xml')
    param.OutputPath = '/home/lijiao/Documents/Modis/output/'
    auxfile = param.OutputPath+param.GetParamDescription()+'_'+'1000'+'_'+param.ProjectTaskName+'.HDF'
    ProcessProj(param,1000,False)

    if os.path.exists(auxfile) == False:
        ProcessAuxProj(1000)
    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,))
    # p2.start()
    #
    # p3 = multiprocessing.Process(target = ProcessProj, args = (param,500,))
    # p3.start()

    # ProcessProj(param, 1000)
    # ProcessProj(param, 500)