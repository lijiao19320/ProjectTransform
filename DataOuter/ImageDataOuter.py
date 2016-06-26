# from DataOuter import *
# from HdfOperator import *
#
# class ImageDataOuter(DataOuter):
#
#     __HdfOperator = HdfOperator()
#
#     def __init__(self):
#         super(HdfDataOuter, self).__init__()
#         return
#
#
#     def Save(self,U,V):
#         savefile = '/mnt/hgfs/Vmware Linux/Data/save.hdf'
#
#         self.__HdfOperator.WriteHdfDataset(savefile, 'tt', 'U', U)
#         self.__HdfOperator.WriteHdfDataset(savefile, 'tt', 'V', V)
#
#         return