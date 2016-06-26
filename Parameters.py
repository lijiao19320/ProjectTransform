from pyproj import Proj, transform

class ProjParameters(object):

    SrcProj = Proj(proj='longlat',ellps='WGS84')

    DstProj = Proj(proj='lcc',ellps='WGS84')