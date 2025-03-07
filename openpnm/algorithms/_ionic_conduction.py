import logging
import numpy as np
from openpnm.algorithms import ReactiveTransport
from openpnm.models.physics import source_terms as st
from openpnm.utils import Docorator


__all__ = ['IonicConduction']


logger = logging.getLogger(__name__)
docstr = Docorator()


@docstr.get_sections(base='IonicConductionSettings', sections=['Parameters'])
@docstr.dedent
class IonicConductionSettings:
    r"""

    Parameters
    ----------
    %(ReactiveTransportSettings.parameters)s
    charge_conservation : str
        <??>
    """
    quantity = 'pore.potential'
    conductance = 'throat.ionic_conductance'
    charge_conservation = 'electroneutrality'
    cache = False


class IonicConduction(ReactiveTransport):
    r"""
    A class to enforce charge conservation in ionic transport simulations.

    Parameters
    ----------
    network : Network
        The network on which this algorithm operates
    name : str, optional
        A unique name to give the object for easier identification.  If not
        given, one is generated.
    """

    def __init__(self, name='ionic_#', **kwargs):
        super().__init__(name=name, **kwargs)
        self.settings._update(IonicConductionSettings())

    def _charge_conservation_eq_source_term(self, e_alg):
        # Source term for Poisson or charge conservation (electroneutrality) eq
        phase = self.project.phase()[self.settings['phase']]
        Ps = (self['pore.all'] * np.isnan(self['pore.bc.value'])
              * np.isnan(self['pore.bc.rate']))
        mod = st.charge_conservation
        phys = self.project.find_physics(phase=phase)
        phys[0].add_model(propname='pore.charge_conservation', model=mod,
                          phase=phase, p_alg=self, e_alg=e_alg,
                          assumption=self.settings['charge_conservation'])
        self.set_source(propname='pore.charge_conservation', pores=Ps)
