import h5py
import os
import os.path
import numpy as N
from pyhdf.SD import SD, SDC

class HdfOperator(object):



    def Open(self,filePath):
        if 'MOD' in filePath:
            return SD(filePath, SDC.READ)
        else:
            return h5py.File(filePath, 'a')

    def ReadHdfDataset(self,fileHandle,groupPath,datasetPath):
        dataset = N.zeros((1,1,1))
        if (groupPath in fileHandle.keys()) or groupPath == '/':
            hdfgroup = fileHandle[groupPath]
            # if datasetPath in hdfgroup.keys():
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


        if type(attrValue) is str:
            hdfgroup.attrs[attrName]=  N.string_(attrValue)
        else:
            hdfgroup.attrs[attrName] = attrValue
        return

    def WriteHdfDatasetAttribute(self, fileHandle,grouppath,dataset, attrName, attrValue):

        hdfgroup = fileHandle[grouppath]
        dataset = hdfgroup[dataset]
        if type(attrValue) is str:
            dataset.attrs[attrName]=  N.string_(attrValue)
        else:
            dataset.attrs[attrName] = attrValue
        return

    def Close(self,hdfFile):
        hdfFile.close()
