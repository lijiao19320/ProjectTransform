from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *


param = ProjParameters()
# param.DstProj = Proj(proj='latlong',datum='WGS84',lon_0=145)
param.DstProj = Proj(proj='merc',datum='WGS84',lon_0=145)

# u,v = param.DstProj(100,40)
# print u,v
#
# print param.DstProj(u,v,inverse=True)
# param.ProjRange = ProjRange(0,60,70,140)
param.ProjRange = ProjRange(0,60,70,140)
param.OutputPath = '/mnt/hgfs/Vmware Linux/Data/'

# file = '/mnt/hgfs/Vmware Linux/Data/FY3A_VIRRX_GBAL_L1_20090427_0255_1000M_MS.HDF'
provider = H8Dataprovider()
#4km
# file = ['/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf']
# file.append('/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf')
# file.append('/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_4000M_NOM_20160414_0500.hdf')

#2km
L1file = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_2000M_NOM_20160714_2000.hdf'
path, filename = os.path.split(L1file)
InputString = filename.upper().replace('.HDF', '')

provider.SetL1File(L1file)
provider.SetLonLatFile('/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf',
                        '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf')
provider.SetInputString(InputString)

#500m
# file = ['/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LAT.hdf']
# file.append('/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_500M_NOM_LON.hdf')
# file.append('/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_0500M_NOM_20160728_0800.hdf')

#AuxilaryData

# Lonfile='/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001(2000).hdf'
# Latfile = '/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002(2000).hdf'
# LNDfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_LND_2000M.HDF'
# LMKfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_LMK_2000M.HDF'
# DEMfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_DEM_2000M.HDF'
# COASTfile = '/mnt/hgfs/Vmware Linux/Data/IFL_FY4A_AGRIX_COAST_2000M.HDF'
# SATZENfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_2000M_NOM_SATZEN.HDF'
# SATAZIfile = '/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_2000M_NOM_SATAZI.HDF'
#
# provider.SetLonLatFile(Lonfile,Latfile)
# provider.SetAuxiliaryDataFile(LNDfile,LMKfile,DEMfile,COASTfile,SATZENfile,SATAZIfile,Lonfile,Latfile)
# provider.SetInputString(param.GetParamID())

# print param.ProjRange
# provider = FY3AVirrProvider()
# provider.SetL1File(file)





dataouter = HdfDataOuter()


processor = ProjProcessor(provider,dataouter,param)

processor.PerformProj()


