from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *

# file = '/mnt/hgfs/Vmware Linux/Data/FY3A_VIRRX_GBAL_L1_20090427_0255_1000M_MS.HDF'
file = ['/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000001.hdf']
file.append('/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf')
file.append('/mnt/hgfs/Vmware Linux/Data/AHI8_OBI_4000M_NOM_20160414_0500.hdf')


provider = H8Dataprovider()
# provider = FY3AVirrProvider()
provider.SetFile(file)
provider.SetRange(-80,80,0,0)


param = ProjParameters()
param.DstProj = Proj(proj='merc',datum='WGS84',lon_0=145)

dataouter = HdfDataOuter()


processor = ProjProcessor()
processor.SetDataProvider(provider)
processor.SetProjParameters(param)
processor.SetDataOut(dataouter)


UV = processor.PerformProj()


#pj = Proj(proj='lcc',ellps='WGS84')

#for i in range(1,2749):
    #print ' '
#    latlon = N.hstack((latlon,pj(latData[i, :], lonData[i, :])))

#latlon = pj(latData[:,:],lonData[:,:])

#savefile = '/mnt/hgfs/Vmware Linux/Data/save.hdf'

#HdfOperator.WriteHdfDataset(savefile, 'tt', 'test', latlon)

# def a(b, c):
#     """
#     iwikwiw
#
#     :param b:
#
#     :param c:
#     :return:
#     """
#
#
#
# a(1,2)