"""Contains the test for PATA - Trailer Alarm
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestTrailerAlarm(Rh850Base):
    """
    This class holds the test case for PATA - Trailer Alarm.
    """

    trailer_arming_inputs = [
        ('enbl', 'nrml', 'on', 'act'),
        ('disbl', 'nrml', 'on', 'inact'),
        ('enbl', 'ff', 'on', 'inact'),
        ('enbl', 'tprt', 'on', 'inact'),
        ('enbl', 'rcm', 'on', 'inact'),
        ('enbl', 'fif', 'on', 'inact'),
        ('enbl', 'fts', 'on', 'inact'),
        ('enbl', 'ft', 'on', 'inact'),
        ('enbl', 'nrml', 'off', 'inact')]

    @slash.parametrize(('tccm2', 'lcmda', 'octas', 'alarmstat'), trailer_arming_inputs)
    def test_arming_trailer_alarm(self, tccm2, lcmda, octas, alarmstat):
        """
        Run Test - test_arming_trailer_alarm
        https://ford.atlassian.net/browse/ZOPRO-26703
        https://ford.atlassian.net/browse/ZOPRO-26705
        """

        result = self.execute_vlab_test("test_arming_trailer_alarm",
                                        inputs=f"{tccm2}::{lcmda}::{octas}",
                                        outputs=f"{alarmstat}",)
        self._assert_return_code(result)

    trailer_kol_behaviour_input = [
        ('end', 'no', 'arm'),
        ('run', 'no', 'act'),
        ('end', 'yes', 'arm'),
    ]

    @slash.parametrize(('tat', 'trailer_connection', 'alrmstat'), trailer_kol_behaviour_input)
    def test_trailer_kol_behaviour(self, tat, trailer_connection, alrmstat):
        """
        Run Test - test_trailer_kol_behaviour
        https://ford.atlassian.net/browse/ZOPRO-26704
        """

        result = self.execute_vlab_test("test_trailer_kol_behaviour",
                                        inputs=f"{tat}::{trailer_connection}::{alrmstat}")
        self._assert_return_code(result)

    disarming_trailer_alarm_input = [
        ('arm', 'off', 'inactive'),
        ('act', 'off', 'inactive'),
    ]

    @slash.parametrize(('pre_alrmstat', 'tas', 'traileralarm_stat'), disarming_trailer_alarm_input)
    def test_disarming_trailer_alarm_with_traileralarmsetting(self, pre_alrmstat,
                                                              tas, traileralarm_stat):
        """
        Run Test - test_disarming_trailer_alarm_with_traileralarmsetting
        https://ford.atlassian.net/browse/ZOPRO-26708
        """
        result = self.execute_vlab_test("test_disarming_trailer_alarm_with_traileralarmsetting",
                                        inputs=f"{pre_alrmstat}::{tas}::{traileralarm_stat}")
        self._assert_return_code(result)

    def test_disarming_trailer_alarm_with_disarmed_mode(self):
        """
        Run Test - test_disarming_trailer_alarm_with_disarmed_mode
        https://ford.atlassian.net/browse/ZOPRO-26708
        """
        result = self.execute_vlab_test("test_disarming_trailer_alarm_with_disarmed_mode")
        self._assert_return_code(result)
