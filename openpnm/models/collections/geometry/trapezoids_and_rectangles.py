import openpnm.models as mods
from openpnm.utils import get_model_collection


def trapezoids_and_rectangles(regen_mode=None, domain=None):
    return get_model_collection(collection=_trapezoids_and_rectangles,
                                regen_mode=regen_mode,
                                domain=domain)


_trapezoids_and_rectangles = {
    'pore.seed': {
        'model': mods.misc.random,
        'element': 'pore',
        'num_range': [0.2, 0.7],
        'seed': None,
    },
    'pore.max_size': {
        'model': mods.geometry.pore_size.largest_sphere,
        'iters': 10,
    },
    'pore.diameter': {
        'model': mods.misc.product,
        'props': ['pore.max_size', 'pore.seed'],
    },
    'pore.volume': {
        'model': mods.geometry.pore_volume.circle,
        'pore_diameter': 'pore.diameter',
    },
    'throat.max_size': {
        'model': mods.misc.from_neighbor_pores,
        'mode': 'min',
        'prop': 'pore.diameter',
    },
    'throat.diameter': {
        'model': mods.misc.scaled,
        'factor': 0.5,
        'prop': 'throat.max_size',
    },
    'throat.length': {
        'model': mods.geometry.throat_length.trapezoids_and_rectangles,
        'pore_diameter': 'pore.diameter',
        'throat_diameter': 'throat.diameter',
    },
    'throat.volume': {
        'model': mods.geometry.throat_volume.rectangle,
        'throat_diameter': 'throat.diameter',
        'throat_length': 'throat.length',
    },
    'throat.cross_sectional_area': {
        'model': mods.geometry.throat_cross_sectional_area.rectangle,
        'throat_diameter': 'throat.diameter',
    },
    'throat.diffusive_size_factors': {
        'model': mods.geometry.diffusive_size_factors.trapezoids_and_rectangles,
        'pore_diameter': 'pore.diameter',
        'throat_diameter': 'throat.diameter',
    },
    'throat.hydraulic_size_factors': {
        'model': mods.geometry.hydraulic_size_factors.trapezoids_and_rectangles,
        'pore_diameter': 'pore.diameter',
        'throat_diameter': 'throat.diameter',
    },
}
