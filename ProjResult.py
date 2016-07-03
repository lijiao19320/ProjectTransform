import numpy as N


class ProjResult(object):

    __U = None
    __V = None

    def getU(self):
        return  self.__U

    def setU(self,value):
        self.__U = value

    U = property(getU, setU)

    def getV(self):
        return  self.__V

    def setV(self,value):
        self.__V = value

    V = property(getV, setV)

    __ResultInfo = None

    @property
    def ResultInfo(self):
        return  self.__ResultInfo


    @ResultInfo.setter
    def ResultInfo(self, new_value):
        self.__ResultInfo = new_value
