from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *
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

    Latfile='/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'

    if resolution == 1000:
        Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf'
        Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf'
    elif resolution ==500:
        Latfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LON.HDF'

    LNDfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'
    LMKfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'
    DEMfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'
    COASTfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'
    SATZENfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'
    SATAZIfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'

    provider.SetLonLatFile(Latfile,Lonfile)
    provider.SetAuxiliaryDataFile(LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Latfile,Lonfile)
    # provider.SetInputString(param.GetParamID())
    return  provider

def CreateStdProjProvider(resolution):
    provider = H8Dataprovider()

    Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
    Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'
    L1file = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_2000M_NOM_' + sys.argv[1] + '.hdf'
    InputString = 'AHI8_OBI_2000M_NOM_' + sys.argv[1]
    if resolution == 1000:
        Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf'
        Lonfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf'
        L1file = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_1000M_NOM_' + sys.argv[1] + '.hdf'
        InputString = 'AHI8_OBI_1000M_NOM_' + sys.argv[1]
    elif resolution == 500:
        Latfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LAT.HDF'
        Lonfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LON.HDF'
        L1file = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_0500M_NOM_' + sys.argv[1] + '.hdf'
        InputString = 'AHI8_OBI_0500M_NOM_' + sys.argv[1]

    provider.SetLonLatFile(Latfile,
                           Lonfile)

    print sys.argv[1]
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
    auxparam = paramparser.parseXML('/mnt/hgfs/Vmware Linux/Data/' + sys.argv[2])
    auxparam.OutputPath = '/mnt/hgfs/Vmware Linux/Data/'
    auxparam.ProjectResolution = resolution
    ProcessProj(auxparam, resolution, True)


if __name__ == '__main__':



    paramparser = ParameterParser()
    param = paramparser.parseXML('/mnt/hgfs/Vmware Linux/Data/'+sys.argv[2])
    param.OutputPath = '/mnt/hgfs/Vmware Linux/Data/'
    auxfile = param.OutputPath+param.GetParamDescription()+'_2000_Proj.HDF'
    ProcessProj(param, int(sys.argv[3]),False)

    if os.path.exists(auxfile) == False:
        ProcessAuxProj(int(sys.argv[3]))
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