import os
import py
import copy
import json
import pytest
import numpy as np
import openpnm as op
from pathlib import Path
from openpnm.io import network_from_jsongraph, network_to_jsongraph


class JSONGraphTest:

    def setup_class(self):
        ws = op.Workspace()
        ws.settings['local_data'] = True
        self.net = op.network.Cubic(shape=[2, 2, 2])
        self.net['pore.diameter'] = 2.0 * np.ones(self.net.Np)
        self.net['throat.diameter'] = 2.0 * np.ones(self.net.Nt)
        self.net.add_model(propname='throat.length',
                           model=op.models.network.pore_to_pore_distance)

    def teardown_class(self):
        ws = op.Workspace()
        ws.clear()

    # def test_save_failure(self, tmpdir):
    #     path = Path(os.path.realpath(tmpdir),
    #                 '../../../fixtures/JSONGraphFormat')
    #     filename = Path(path.resolve(), 'save_failure.json')

    #     # Create a deep copy of network with one required property missing
    #     net = copy.deepcopy(self.net)
    #     net.pop('pore.diameter')

    #     # Ensure an exception was thrown
    #     with pytest.raises(Exception) as e_info:
    #         op.io.network_to_jsongraph(net.project, filename=filename)
    #     expected_error = 'Error - network is missing one of:'
    #     assert expected_error in str(e_info.value)

    def test_save_success(self):
        path = Path(os.path.realpath(__file__),
                    '../../../fixtures/JSONGraphFormat')
        filename = Path(path.resolve(), 'save_success.json')
        op.io.network_to_jsongraph(self.net, filename=filename)

        # Read newly created file
        with open(filename, 'r') as file:
            json_file = json.load(file)

        # Ensure correctnes of overal network properties
        assert json_file['graph']['metadata']['number_of_nodes'] == self.net.Np
        assert json_file['graph']['metadata']['number_of_links'] == self.net.Nt

        # Ensure correctnes of node list properties
        nodes = sorted(json_file['graph']['nodes'], key=lambda node: int(node['id']))
        assert len(nodes) == self.net.Np
        assert isinstance(nodes, list)

        # Sweep all nodes in the list
        for node in nodes:
            assert isinstance(node, dict)

            # Ensure correctnes of node property types
            assert 'id' in node
            assert 'metadata' in node
            assert isinstance(node['id'], str)
            assert isinstance(node['metadata'], dict)

            # Ensure correctnes of node property values
            assert int(node['id']) < self.net.Np

            # Ensure correctnes of node metadata types
            assert 'node_coordinates' in node['metadata']
            assert 'node_squared_radius' in node['metadata']
            assert 'x' in node['metadata']['node_coordinates']
            assert 'y' in node['metadata']['node_coordinates']
            assert 'z' in node['metadata']['node_coordinates']
            assert isinstance(node['metadata']['node_coordinates'], dict)
            assert isinstance(node['metadata']['node_squared_radius'], int)
            assert isinstance(node['metadata']['node_coordinates']['x'], int)
            assert isinstance(node['metadata']['node_coordinates']['y'], int)
            assert isinstance(node['metadata']['node_coordinates']['z'], int)

            # Ensure correctness of node metadata values
            assert node['metadata']['node_squared_radius'] == 1
            assert node['metadata']['node_coordinates']['x'] * 2 % 2 == 0
            assert node['metadata']['node_coordinates']['y'] * 2 % 2 == 0
            assert node['metadata']['node_coordinates']['z'] * 2 % 2 == 0

        # Ensure correctnes of edge list properties
        edges = sorted(json_file['graph']['edges'], key=lambda edge: int(edge['id']))
        assert len(edges) == self.net.Nt
        assert isinstance(edges, list)

        # Sweep all edges in the list
        for edge in edges:
            assert isinstance(edge, dict)

            # Ensure correctnes of edge property types
            assert 'id' in edge
            assert 'source' in edge
            assert 'target' in edge
            assert 'metadata' in edge
            assert isinstance(edge['id'], str)
            assert isinstance(edge['source'], str)
            assert isinstance(edge['target'], str)
            assert isinstance(edge['metadata'], dict)

            # Ensure correctnes of edge property values
            assert int(edge['id']) < self.net.Nt
            assert int(edge['source']) < self.net.Np
            assert int(edge['target']) < self.net.Np

            # Ensure correctnes of edge metadata types
            assert 'link_length' in edge['metadata']
            assert 'link_squared_radius' in edge['metadata']
            assert isinstance(edge['metadata']['link_length'], float)
            assert isinstance(edge['metadata']['link_squared_radius'], float)

            # Ensure correctnes of edge metadata values
            assert edge['metadata']['link_length'] == 1.0
            assert edge['metadata']['link_squared_radius'] == 1.0

        # Remove test file after completion
        os.remove(filename)

    def test_load_failure(self):
        path = Path(os.path.realpath(__file__),
                    '../../../fixtures/JSONGraphFormat')
        filename = Path(path.resolve(), 'invalid.json')

        # Ensure an exception was thrown
        with pytest.raises(Exception):
            op.io.from_jsongraph(filename)

    def test_load_success(self):
        # Load JSON file and ensure project integrity
        path = Path(os.path.realpath(__file__),
                    '../../../fixtures/JSONGraphFormat')
        filename = Path(path.resolve(), 'valid.json')
        net = op.io.network_from_jsongraph(filename)
        assert hasattr(net, 'conns')

        # Ensure overal network properties
        assert net.Np == 2
        assert net.Nt == 1

        # Ensure correctness of pore properties
        assert np.array_equal(net['pore.index'], np.array([0, 1]))
        assert np.array_equal(net['pore.diameter'], np.array([0, 0]))
        assert np.array_equal(net['pore.coords'][0], np.array([0, 0, 0]))
        assert np.array_equal(net['pore.coords'][1], np.array([1, 1, 1]))

        # Ensure correctness of throat properties
        length = 1.73205080757
        squared_radius = 5.169298742047715
        assert net['throat.length'] == length
        assert np.array_equal(net['throat.conns'], np.array([[0, 1]]))
        assert net['throat.diameter'] == 2.0 * np.sqrt(squared_radius)


if __name__ == '__main__':
    # All the tests in this file can be run with 'playing' this file
    t = JSONGraphTest()
    self = t  # For interacting with the tests at the command line
    tmpdir = py.path.local()
    t.setup_class()
    for item in t.__dir__():
        if item.startswith('test'):
            print(f'Running test: {item}')
            try:
                t.__getattribute__(item)()
            except TypeError:
                t.__getattribute__(item)()
