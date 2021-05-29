from ansys.mapdl.core import LocalMapdlPool

pool = LocalMapdlPool(10)
from ansys.mapdl.core import examples

files = [examples.vmfiles['vm%d' % i] for i in range(1, 21)]

outputs = pool.run_batch(files)

len(outputs)
