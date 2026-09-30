"""Contains the test for PATA - PreArmed Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestPrearmedMode(Rh850Base):
    """
    This class holds the test case for PATA - PreArmed Mode.
    """

    prearmed_mode_inputs = [
        "enbl-nrml-vpm40-def-cen_lck-rem-val1-prearm",
        "enbl-nrml-vpm40-def-cen_lck-ext-val1-prearm",
        "enbl-nrml-vpm40-def-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm40-rej-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm40-err-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm40-cnf-cen_lck-cell-val1-disarm",
        "enbl-nrml-vpm10-def-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm20-def-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm50-def-cen_lck-cell-val1-prearm",
        "enbl-nrml-vpm60-def-cen_lck-cell-val1-disarm",
        "enbl-nrml-vpm70-def-cen_lck-cell-val1-disarm",
        "disbl-nrml-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-ff-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-tprt-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-rcm-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-fif-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-fts-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-ft-vpm40-def-cen_lck-cell-val1-disarm",
        "enbl-nrml-vpm40-def-cen_lck-cell-val0-disarm"
    ]

    @slash.parametrize('prearmed_input', prearmed_mode_inputs)
    def test_prearmed_mode(self, prearmed_input):
        """
        Run Test - test_prearmed_mode
        https://ford.atlassian.net/browse/ZOPRO-26897
        https://ford.atlassian.net/browse/ZOPRO-22338
        """

        result = self.execute_vlab_test("test_prearmed_mode",
                                        inputs=prearmed_input)
        self._assert_return_code(result)
