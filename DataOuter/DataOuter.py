import sys
from abc import ABCMeta, abstractmethod


class DataOuter(object):

    __UV = []

    def __init__(self):
        return

    @abstractmethod
    def Save(self,projResult,dataProvider):
        pass

