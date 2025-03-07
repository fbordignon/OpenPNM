import logging
# from collections import ChainMap  # Might use eventually
from openpnm.phase.mixtures import GenericMixture
import openpnm.models as mods
from openpnm.utils import Docorator
docstr = Docorator()
logger = logging.getLogger(__name__)


@docstr.dedent
class IdealGas(GenericMixture):
    r"""
    Creates Mixture object that represents a ideal gas system
    consisting of a given list of Phases as components.

    Parameters
    ----------
    %(GenericMixture.parameters)s

    """

    def __init__(self, name='mix_#', **kwargs):
        super().__init__(name=name, **kwargs)
        self.add_model(propname='pore.molar_density',
                       model=mods.phase.molar_density.ideal_gas,
                       regen_mode='deferred')
