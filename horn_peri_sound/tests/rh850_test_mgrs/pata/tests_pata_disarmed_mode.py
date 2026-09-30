"""Contains the test for PATA - DisArmed Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestDisArmedMode(Rh850Base):
    """
    This class holds the test case for PATA - DisArmed Mode.
    """

    disarmed_mode_lcmda_inputs = [
        ('fts', 'disarm'),
        ('tprt', 'disarm'),
        ('nrml', 'prearm'),
        ('ff', 'disarm'),
        ('rcm', 'disarm'),
        ('fif', 'disarm'),
        ('ft', 'disarm')]

    @slash.parametrize(('lcmda', 'alrmstat'), disarmed_mode_lcmda_inputs)
    def test_disarmed_mode_with_lifecyclemode(self, lcmda, alrmstat):
        """
        Run Test - test_disarmed_mode_with_lifecyclemode
        https://ford.atlassian.net/browse/ZOPRO-26899
        """

        result = self.execute_vlab_test("test_disarmed_mode_with_lifecyclemode",
                                        inputs=f"{lcmda}", outputs=f"{alrmstat}",)
        self._assert_return_code(result)

    disarmed_mode_vpm_inputs = [
        ('vpm50', 'prearm'),
        ('vpm60', 'disarm'),
        ('vpm70', 'disarm'),
        ('vpm10', 'prearm'),
        ('vpm20', 'prearm'),
        ('vpm40', 'prearm')
    ]

    @slash.parametrize(('vpm', 'alrmstat'), disarmed_mode_vpm_inputs)
    def test_disarmed_mode_with_vehiclepowermode(self, vpm, alrmstat):
        """
        Run Test - test_disarmed_mode_with_vehiclepowermode
        https://ford.atlassian.net/browse/ZOPRO-26899
        """

        result = self.execute_vlab_test("test_disarmed_mode_with_vehiclepowermode",
                                        inputs=f"{vpm}", outputs=f"{alrmstat}",)
        self._assert_return_code(result)

    disarmed_mode_evls_inputs = [
        ('prearm', 'cen_unlck', 'int', 'disarm'),
        ('prearm', 'cen_unlck', 'ext', 'disarm'),
        ('prearm', 'cen_unlck', 'cell', 'disarm'),
        ('prearm', 'cen_unlck', 'rem', 'disarm'),
        ('prearm', 'cen_unlck', 'eme', 'prearm'),
        ('prearm', 'cen_unlck', 'wo_req', 'prearm'),
        ('prearm', 'cen_lck', 'int', 'prearm'),
        ('prearm', 'par_lck', 'int', 'prearm'),
        ('arm', 'cen_unlck', 'ext', 'disarm'),
        ('arm', 'cen_unlck', 'cell', 'disarm'),
        ('arm', 'cen_unlck', 'rem', 'disarm'),
        ('arm', 'cen_unlck', 'int', 'arm'),
        ('arm', 'cen_unlck', 'eme', 'arm'),
        ('arm', 'cen_unlck', 'wo_req', 'arm'),
        ('act', 'cen_unlck', 'ext', 'disarm'),
        ('act', 'cen_unlck', 'cell', 'disarm'),
        ('act', 'cen_unlck', 'rem', 'disarm'),
        ('act', 'cen_unlck', 'int', 'act'),
        ('act', 'cen_unlck', 'eme', 'act'),
        ('act', 'cen_unlck', 'wo_req', 'act'),

    ]

    @slash.parametrize(('pre_cond', 'evls', 'llur', 'alrmstat'), disarmed_mode_evls_inputs)
    def test_disarmed_mode_with_exteriorvehiclelockstatus(self, pre_cond, evls, llur, alrmstat):
        """
        Run Test - test_disarmed_mode_with_exteriorvehiclelockstatus
        https://ford.atlassian.net/browse/ZOPRO-26899
        """

        result = self.execute_vlab_test("test_disarmed_mode_with_exteriorvehiclelockstatus",
                                        inputs=f"{pre_cond}::{evls}::{llur}",
                                        outputs=f"{alrmstat}",)
        self._assert_return_code(result)

    disarmed_mode_patiallylocked_inputs = [
        'prearm-par_lck-val0-unlck-disarm',
        'prearm-par_lck-val1-unlck-prearm',
        'prearm-par_lck-val0-lck-prearm',
        'prearm-par_lck-val0-na-prearm',
        'prearm-par_lck-val0-fal-prearm',
        'arm-par_lck-val0-unlck-disarm',
        'arm-par_lck-val1-unlck-arm',
        'arm-par_lck-val0-lck-arm',
        'arm-par_lck-val0-na-arm',
        'arm-par_lck-val0-fal-arm',
        'act-par_lck-val0-unlck-disarm',
        'act-par_lck-val1-unlck-act',
        'act-par_lck-val0-lck-act',
        'act-par_lck-val0-na-act',
        'act-par_lck-val0-fal-act',
    ]

    @slash.parametrize('disarmed_mode_partiallylocked_inpt', disarmed_mode_patiallylocked_inputs)
    def test_disarmed_mode_with_patilaly_locked(self, disarmed_mode_partiallylocked_inpt):
        """
        Run Test - test_disarmed_mode_with_patilaly_locked
        https://ford.atlassian.net/browse/ZOPRO-26899
        """

        result = self.execute_vlab_test("test_disarmed_mode_with_patilaly_locked",
                                        inputs=disarmed_mode_partiallylocked_inpt)
        self._assert_return_code(result)
