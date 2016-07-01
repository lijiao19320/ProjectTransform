import h5py
import os
import os.path

class HdfOperator(object):



    def Open(self,filePath):
        return h5py.File(filePath, 'a')

    def ReadHdfDataset(self,fileHandle,groupPath,datasetPath):

        hdfgroup = fileHandle[groupPath]
        dataset = hdfgroup[datasetPath]
        return dataset

    def WriteHdfDataset(self,fileHandle,groupPath,datasetName,dataset):


        # if os.path.exists(filePath):
        #     os.remove(filePath)

        hdfgroup = fileHandle.require_group(groupPath)
        hdfgroup.create_dataset(datasetName,data=dataset)

    def WriteHdfAttribute(self):
        return 

    def Close(self,hdfFile):
        hdfFile.close()
