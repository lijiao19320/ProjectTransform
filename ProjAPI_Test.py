from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *


param = ProjParameters()
param.DstProj = Proj(proj='merc',datum='WGS84',lon_0=145)
# param.ProjRange = ProjRange(0,60,70,140)
param.ProjRange = ProjRange(-60,60,-180,180)


# file = '/mnt/hgfs/Vmware Linux/Data/FY3A_VIRRX_GBAL_L1_20090427_0255_1000M_MS.HDF'
file = ['/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf']
file.append('/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf')
file.append('/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_4000M_NOM_20160414_1900.hdf')


provider = H8Dataprovider()
# provider = FY3AVirrProvider()
provider.SetFile(file)





dataouter = HdfDataOuter()


processor = ProjProcessor(provider,dataouter,param)

processor.PerformProj()


# todo：关于参数的解析，还是设计成xml的语言把，以前的实在是可读性太差，然后在写一个转换的函数作兼容