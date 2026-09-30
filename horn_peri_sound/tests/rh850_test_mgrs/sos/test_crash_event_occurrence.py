"""Contains the test for SOS - Crash Event Occurrence
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestCrashEventOccurrence(Rh850Base):
    """
    This class holds the test case for SOS Post Crash Alert - Event Occurrence.
    """

    crash_event_ocurrence_inputs_1 = [
        "no_event",
        "fuel_cutoff_event",
        "deploy_event",
        "invalid"
    ]

    @slash.parametrize("crash_event_ocurrence_inputs", crash_event_ocurrence_inputs_1)
    def test_crash_event_occurrence_1(self, crash_event_ocurrence_inputs):
        """
        Run Test - test_crash_event_occurrence
        https://ford.atlassian.net/browse/ZOPRO-28367
        """

        result = self.execute_vlab_test("test_crash_event_occurrence_1",
                                        inputs=crash_event_ocurrence_inputs)
        self._assert_return_code(result)

    crash_event_occurrence_inputs_2 = [
        "true",
        "false",
    ]

    @slash.parametrize("crash_event_occurrence_inp_2", crash_event_occurrence_inputs_2)
    def test_crash_event_occurrence_2(self, crash_event_occurrence_inp_2):
        """
        Run Test - test_crash_event_occurrence_2
        https://ford.atlassian.net/browse/ZOPRO-28367
        """

        result = self.execute_vlab_test("test_crash_event_occurrence_2",
                                        inputs=crash_event_occurrence_inp_2)
        self._assert_return_code(result)
