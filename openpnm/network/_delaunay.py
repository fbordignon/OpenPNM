import numpy as np
from openpnm.network import Network
from openpnm.utils import Docorator
from openpnm._skgraph.generators import delaunay, tools
from openpnm._skgraph.tools import isoutside
from openpnm._skgraph.operations import trim_nodes


__all__ = ['Delaunay']
docstr = Docorator()


@docstr.dedent
class Delaunay(Network):
    r"""
    Random network formed by Delaunay tessellation of arbitrary base points

    Parameters
    ----------
    points : array_like or int
        Can either be an N-by-3 array of point coordinates which will be used,
        or a scalar value indicating the number of points to generate
    shape : array_like
        The size of the domain.  It's possible to create cubic as well as 2D
        square domains by changing the ``shape`` as follows:

        ========== ============================================================
        shape      result
        ========== ============================================================
        [x, y, z]  A 3D cubic domain of dimension x, y and z
        [x, y, 0]  A 2D square domain of size x by y
        [r, z]     A 3D cylindrical domain of radius r and height z
        [r, 0]     A 2D circular domain of radius r
        [r]        A 3D spherical domain of radius r
        ========== ============================================================

    %(Network.parameters)s

    See Also
    --------
    Gabriel
    Voronoi
    DelaunayVoronoiDual

    Notes
    -----
    This class always performs the tessellation on the full set of points,
    then trims any points that lie outside the given domain ``shape``.

    """

    def __init__(self, shape=[1, 1, 1], points=None, **kwargs):
        super().__init__(**kwargs)
        points = tools.parse_points(shape=shape, points=points)
        net, tri = delaunay(points=points, shape=shape,
                            node_prefix='pore', edge_prefix='throat')
        Ps = isoutside(net, shape=shape)
        net = trim_nodes(g=net, inds=Ps)
        self.update(net)


if __name__ == "__main__":
    import openpnm as op
    dn = Delaunay(shape=[1, 0], points=500)
    op.topotools.plot_connections(dn)
