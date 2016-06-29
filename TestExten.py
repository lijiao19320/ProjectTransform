import cos_module_np
import numpy as N


tu = N.ones((10, 10))
tv = N.ones((10, 10))
refdata = N.ones((10, 10))

test = cos_module_np.cos_func_np(3, 4, tu, tv, refdata)
