"""Contains the test for PATA - Activated Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestActivatedMode(Rh850Base):
    """
    This class holds the test case for PATA - Activated Mode.
    """

    activated_mode_inputs = [
        ("df", "ajar", "df_door", "act"),
        ("df", "clsd", "null", "arm"),
        ("df", "fal", "null", "arm"),
        ("df", "unk", "null", "arm"),
        ("df", "na", "null", "arm"),
        ("pf", "ajar", "pf_door", "act"),
        ("pf", "clsd", "null", "arm"),
        ("pf", "fal", "null", "arm"),
        ("pf", "unk", "null", "arm"),
        ("pf", "na", "null", "arm"),
        ("dr", "ajar", "dr_door", "act"),
        ("dr", "clsd", "null", "arm"),
        ("dr", "fal", "null", "arm"),
        ("dr", "unk", "null", "arm"),
        ("dr", "na", "null", "arm"),
        ("pr", "ajar", "pr_door", "act"),
        ("pr", "clsd", "null", "arm"),
        ("pr", "fal", "null", "arm"),
        ("pr", "unk", "null", "arm"),
        ("pr", "na", "null", "arm"),
        ("bec", "ajar", "lg_door", "act"),
        ("bec", "clsd", "null", "arm"),
        ("bec", "fal", "null", "arm"),
        ("bec", "unk", "null", "arm"),
        ("bec", "na", "null", "arm"),
        ("fec", "ajar", "hood", "act"),
        ("fec", "clsd", "null", "arm"),
        ("fec", "fal", "null", "arm"),
        ("fec", "unk", "null", "arm"),
        ("fec", "na", "null", "arm")
    ]

    @slash.parametrize(('drid', 'das', 'pes', 'alrmstat'), activated_mode_inputs)
    def test_activated_mode_with_doorajarstatus(self, drid, das, pes, alrmstat):
        """
        Run Test - test_activated_mode_with_doorajarstatus
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26702
                        https://ford.atlassian.net/browse/ZOPRO-11348
                        https://ford.atlassian.net/browse/ZOPRO-26898
                        https://ford.atlassian.net/browse/ZOPRO-11351
                        https://ford.atlassian.net/browse/ZOPRO-22330
                        https://ford.atlassian.net/browse/ZOPRO-22325
                        https://ford.atlassian.net/browse/ZOPRO-22335
        """

        result = self.execute_vlab_test("test_activated_mode_with_doorajarstatus",
                                        inputs=f"{drid}::{das}::{pes}", outputs=f"{alrmstat}", )
        self._assert_return_code(result)

    trailer_connection_inputs = [
        ("yes", "act"),
        ("no", "arm"),
    ]

    @slash.parametrize(('trailerconnection', 'alrmstat'), trailer_connection_inputs)
    def test_activated_mode_with_trailer_diconnected(self, trailerconnection, alrmstat):
        """
        Run Test - test_activated_mode_with_trailer_diconnected
        https://ford.atlassian.net/browse/ZOPRO-26898
        https://ford.atlassian.net/browse/ZOPRO-26702
        """

        result = self.execute_vlab_test("test_activated_mode_with_trailer_diconnected",
                                        inputs=f"{trailerconnection}", outputs=f"{alrmstat}")
        self._assert_return_code(result)
