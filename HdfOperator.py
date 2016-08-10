import h5py
import os
import os.path
import numpy as N

class HdfOperator(object):



    def Open(self,filePath):
        return h5py.File(filePath, 'a')

    def ReadHdfDataset(self,fileHandle,groupPath,datasetPath):
        dataset = N.zeros((1,1,1))
        if groupPath in fileHandle.keys():
            hdfgroup = fileHandle[groupPath]
            if datasetPath in hdfgroup.keys():
                dataset = hdfgroup[datasetPath]
        return dataset

    def ReadHdfAttri(self,fileHandle,groupPath,attrName):
        hdfgroup = fileHandle[groupPath]
        return hdfgroup.attrs[attrName]


    def WriteHdfDataset(self,fileHandle,groupPath,datasetName,dataset):


        # if os.path.exists(filePath):
        #     os.remove(filePath)

        hdfgroup = fileHandle.require_group(groupPath)
        hdfgroup.create_dataset(datasetName,data=dataset)

    def WriteHdfGroupAttribute(self, fileHandle, attrName, attrValue):
        hdfgroup = fileHandle.require_group('/')
        hdfgroup.attrs[attrName]= attrValue
        return

    def WriteHdfDatasetAttribute(self, fileHandle,grouppath,dataset, attrName, attrValue):

        hdfgroup = fileHandle[grouppath]
        dataset = hdfgroup[dataset]
        dataset.attrs[attrName] = attrValue
        return

    def Close(self,hdfFile):
        hdfFile.close()
