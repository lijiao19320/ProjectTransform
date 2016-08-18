import sys
from abc import ABCMeta, abstractmethod


class DataOuter(object):


    def __init__(self):
        self.__UV = []

        self.__Parameter = None
        return

    @abstractmethod
    def Dispose(self):
        pass

    @abstractmethod
    def Save(self,projResult,dataProvider):
        pass



    def setParameter(self, parameter):
        parameter.register(self)
        self.__Parameter = parameter
        return

    def getParameter(self):
        return self.__Parameter

    Parameter = property(getParameter, setParameter)

    def OnParametersUpdate(self):

        return