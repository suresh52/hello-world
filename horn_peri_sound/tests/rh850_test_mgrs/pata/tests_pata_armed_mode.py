"""Contains the test for PATA - Armed Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestArmedMode(Rh850Base):
    """
    This class holds the test case for PATA - Armed Mode.
    """

    armed_mode_inputs = [
        ('cen_lck', 'rem', 'val0', 'arm'),
        ('cen_lck', 'ext', 'val0', 'arm'),
        ('cen_lck', 'cell', 'val0', 'arm'),
        ('cen_lck', 'int', 'val0', 'act'),
        ('cen_lck', 'eme', 'val0', 'act'),
        ('cen_lck', 'wo_req', 'val0', 'act'),
        ('cen_unlck', 'rem', 'val0', 'disarm'),
        ('par_lck', 'rem', 'val0', 'act'),
        ('cen_lck', 'wo_req', 'val1', 'act'),
    ]

    @slash.parametrize(('evls', 'llur', 'elec', 'alrmstat'), armed_mode_inputs)
    def test_armed_mode_with_exteriorvehiclelockstatus(self, evls, llur, elec, alrmstat):
        """
        Run Test - test_armed_mode_with_exteriorvehiclelockstatus
        https://ford.atlassian.net/browse/ZOPRO-26896
        """

        result = self.execute_vlab_test("test_armed_mode_with_exteriorvehiclelockstatus",
                                        inputs=f"{evls}::{llur}::{elec}", outputs=f"{alrmstat}", )
        self._assert_return_code(result)

    armed_mode_alarm_cycle_inputs = [
        ('305', 'no'),
        ('306', 'no'),
        ('304', 'no'),
        ('120', 'no'),
    ]

    @slash.parametrize(('tmr', 'das'), armed_mode_alarm_cycle_inputs)
    def test_armed_mode_with_alarmcycle_complettion(self, tmr, das):
        """
        Run Test - test_armed_mode_with_alarmcycle_complettion
        https://ford.atlassian.net/browse/ZOPRO-26896
        """

        result = self.execute_vlab_test("test_armed_mode_with_alarmcycle_complettion",
                                        inputs=f"{tmr}::{das}")
        self._assert_return_code(result)
