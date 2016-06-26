from DataOuter.HdfDataOuter import *
from DataProvider.H8DataProvider import *
from DataProvider.FY3AVirrProvider import *
from ProjProcessor import *

# convert awips221 grid to awips218 coordinate system
# (grids defined at http://www.nco.ncep.noaa.gov/pmb/docs/on388/tableb.html)
file = '/mnt/hgfs/Vmware Linux/Data/FY3A_VIRRX_GBAL_L1_20090427_0255_1000M_MS.HDF'
# file.append('/mnt/hgfs/Vmware Linux/Data/fygatNAV.Himawari08.xxxxxxx.000002.hdf')

# provider = H8Dataprovider()
provider = FY3AVirrProvider()
provider.SetFile(file)

param = ProjParameters()
param.DstProj = Proj(proj='merc',datum='WGS84')

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