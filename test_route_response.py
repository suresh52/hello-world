"""Contains the test for sounder service
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestRouteResponse(Rh850Base):
    """
    This class holds the test case for Sounder service - actuateSounder method.
    """
    route_response_inputs = [
    "INVALID_VAL_100",
    "INVALID_VAL_22"
    ]

    @slash.parametrize('route_res_inp', route_response_inputs)
    def test_ss_route_response(self, route_res_inp):
        """
        This is to test Route response invalid - horn:
        https://ford.atlassian.net/browse/ZOPRO-19201
        """

        result = self.execute_vlab_test("test_ss_route_response", inputs=route_res_inp)
        self._assert_return_code(result)