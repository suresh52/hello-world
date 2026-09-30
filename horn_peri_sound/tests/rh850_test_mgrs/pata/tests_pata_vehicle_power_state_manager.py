"""Contains the test for PATA - Vehicle Power State Manager
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestVehiclePowerStateManager(Rh850Base):
    """
    This class holds the test case for PATA - Vehicle Power State Manager.
    """

    vpsm_input = ['disarm', 'prearm', 'arm', 'act']

    @slash.parametrize('alramstat', vpsm_input)
    def test_vehicle_power_state_manager(self, alramstat):
        """
        Run Test - test_vehicle_power_state_manager
        Requirment ID - https://ford.atlassian.net/browse/ZOPRO-11359
        """
        result = self.execute_vlab_test("test_vehicle_power_state_manager", inputs=alramstat)
        self._assert_return_code(result)
