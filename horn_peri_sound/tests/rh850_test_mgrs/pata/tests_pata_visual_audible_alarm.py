"""Contains the test for PATA - Visual Audible Alarm
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestVisualAudibleAlarm(Rh850Base):
    """
    This class holds the test case for PATA - Visual Audible Alarm.
    """

    visual_outputs_inputs = ['act', 'disarm', 'prearm', 'arm']

    @slash.parametrize('alarmstat', visual_outputs_inputs)
    def test_visual_outputs(self, alarmstat):
        """
        Run Test - test_visual_outputs
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11361
        """
        result = self.execute_vlab_test("test_visual_outputs", inputs=alarmstat)
        self._assert_return_code(result)

    visual_outputs_inputs_2 = ['205', '120']

    @slash.parametrize('tmr', visual_outputs_inputs_2)
    def test_visual_outputs_after_alarmcycle(self, tmr):
        """
        Run Test - test_visual_outputs_after_alarmcycle
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11361
                        https://ford.atlassian.net/browse/ZOPRO-11357

        """
        result = self.execute_vlab_test("test_visual_outputs_after_alarmcycle", inputs=tmr)
        self._assert_return_code(result)

    audible_alarm_m2_config_input = ['disarm', 'prearm', 'arm', 'act']

    @slash.parametrize('alarmstat', audible_alarm_m2_config_input)
    def test_audible_alarm_m2_config(self, alarmstat):
        """
        Run Test - test_audible_alarm_m2_config
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-22339
        """
        result = self.execute_vlab_test("test_audible_alarm_m2_config", inputs=alarmstat)
        self._assert_return_code(result)

    audible_sound_completion_inputs_2 = ['50', '30']

    @slash.parametrize('tmr', audible_sound_completion_inputs_2)
    def test_alarmcycle_completion(self, tmr):
        """
        Run Test - test_alarmcycle_completion
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11357
        """
        result = self.execute_vlab_test("test_alarmcycle_completion", inputs=tmr)
        self._assert_return_code(result)

    audiblesound_inputs = ['disarm', 'prearm', 'arm']

    @slash.parametrize('alarmstat', audiblesound_inputs)
    def test_alarm_cycle_completion_audible_sound(self, alarmstat):
        """
        Run Test - test_alarm_cycle_completion_audible_sound
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11357
        """
        result = self.execute_vlab_test("test_alarm_cycle_completion_audible_sound",
                                        inputs=alarmstat)
        self._assert_return_code(result)

    alarm_defination_inputs = ['act', 'disarm', 'prearm', 'arm']

    @slash.parametrize('alarmstat', alarm_defination_inputs)
    def test_alarmcycle_defination(self, alarmstat):
        """
        Run Test - test_alarmcycle_defination
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11356
        """
        result = self.execute_vlab_test("test_alarmcycle_defination", inputs=alarmstat)
        self._assert_return_code(result)

    audible_output_m2_inputs = [
        ('vehicle_horn', 'act'),
        ('bbs', 'arm'),
        ('bbs', 'act'),
        ('bbs', 'prearm'),
        ('bbs_vehicle_horn', 'arm'),
        ('bbs_vehicle_horn', 'act'),
        ('bbs_vehicle_horn', 'prearm'),
        ('vehicle_horn', 'disarm'),
        ('bbs', 'disarm'),
        ('bbs_vehicle_horn', 'disarm'),
    ]

    @slash.parametrize(('ascm2', 'alarmstat'), audible_output_m2_inputs)
    def test_audible_alarm_output_m2_config(self, ascm2, alarmstat):
        """
        Run Test - test_audible_alarm_output_m2_config
        """
        result = self.execute_vlab_test("test_audible_alarm_output_m2_config",
                                        inputs=f"{ascm2}::{alarmstat}")
        self._assert_return_code(result)
