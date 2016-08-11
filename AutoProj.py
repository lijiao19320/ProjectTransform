from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing




def ProviderFactory(isCreateAuxfile,resolution):
    provider = None
    if isCreateAuxfile:
        provider = CreateAuxilaryProvider(resolution)
    else:
        provider = CreateStdProjProvider(resolution)

    return provider


def CreateAuxilaryProvider(resolution):
    provider = H8Dataprovider()

    Latfile='/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    Lonfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'

    if resolution == 1000:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LAT.hdf'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LON.hdf'
    elif resolution ==500:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LON.HDF'

    LNDfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'
    LMKfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'
    DEMfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'
    COASTfile = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'
    SATZENfile = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'
    SATAZIfile = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Latfile,Lonfile)

    return  provider

def CreateStdProjProvider(resolution):
    provider = H8Dataprovider()

    Latfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    Lonfile = '/FY4COMM/FY4A/COM/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'
    L1file = '/FY4COMM/FY4A/L1/AHI8_OBI_2000M_NOM_' + sys.argv[1] + '.hdf'

    if resolution == 1000:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LAT.hdf'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_1000M_NOM_LON.hdf'
        L1file = '/FY4COMM/FY4A/L1/AHI8_OBI_1000M_NOM_' + sys.argv[1] + '.hdf'

    elif resolution == 500:
        Latfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/FY4COMM/FY4A/COM/AHI8_OBI_500M_NOM_LON.HDF'
        L1file = '/FY4COMM/FY4A/L1/AHI8_OBI_0500M_NOM_' + sys.argv[1] + '.hdf'


    provider.SetLonLatFile(Latfile,
                           Lonfile)

    print sys.argv[1]
    provider.SetL1File(L1file)

    return  provider

def ProcessProj(param,reslution,isCreateAuxfile):

    provider = ProviderFactory(isCreateAuxfile,reslution)

    dataouter = HdfDataOuter()

    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/'
    auxparam.ProjectResolution = resolution
    ProcessProj(auxparam, resolution, True)

if __name__ == '__main__':

    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    param.OutputPath = '/FY4COMM/FY4A/L2/AGRIX/PRJ/'

    # ProcessProj(param, 2000,False)
    #
    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,False,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,False,))
    # p2.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,500,False,))
    # p2.start()
    ProcessProj(param, int(sys.argv[3]),False)
    auxfile = param.OutputPath + param.GetParamDescription() + '_'+sys.argv[3]+'_Proj.HDF'
    if os.path.exists(auxfile) == False:
        ProcessAuxProj(int(sys.argv[3]))

    # auxfile = param.OutputPath + param.GetParamDescription() + '_1000_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(1000)

    # auxfile = param.OutputPath + param.GetParamDescription() + '_500_Proj.HDF'
    # if os.path.exists(auxfile) == False:
    #     ProcessAuxProj(500)

    # p1 = multiprocessing.Process(target = ProcessProj, args = (param,2000,))
    # p1.start()
    #
    # p2 = multiprocessing.Process(target = ProcessProj, args = (param,1000,))
    # p2.start()
    #
    # p3 = multiprocessing.Process(target = ProcessProj, args = (param,500,))
    # p3.start()
    # ProcessProj(param,2000)
    # ProcessProj(param, 1000)
    # ProcessProj(param, 500)