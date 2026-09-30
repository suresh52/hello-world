"""Contains the test for PATA - Inhibit Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestInhibitMode(Rh850Base):
    """
    This class holds the test case for PATA - Inhibit Mode.
    """

    common_inhibit_inp = [
        ('df', 'ajar'),
        ('df', 'clsd'),
        ('df', 'fal'),
        ('df', 'unk'),
        ('df', 'na'),
        ('pf', 'ajar'),
        ('pf', 'clsd'),
        ('pf', 'fal'),
        ('pf', 'unk'),
        ('pf', 'na'),
        ('dr', 'ajar'),
        ('dr', 'clsd'),
        ('dr', 'fal'),
        ('dr', 'unk'),
        ('dr', 'na'),
        ('pr', 'ajar'),
        ('pr', 'clsd'),
        ('pr', 'fal'),
        ('pr', 'unk'),
        ('pr', 'na'),
    ]

    bec_inhibit_inputs = [
        ('fec', 'ajar'),
        ('fec', 'clsd'),
        ('fec', 'fal'),
        ('fec', 'unk'),
        ('fec', 'na'),
    ]

    @slash.parametrize(('drid', 'das'), common_inhibit_inp + bec_inhibit_inputs)
    def test_bec_inhibit_mode(self, drid, das):
        """
        Run Test - test_bec_inhibit_mode
        https://ford.atlassian.net/browse/ZOPRO-26906
        """

        result = self.execute_vlab_test("test_bec_inhibit_mode", inputs=f"{drid}::{das}")
        self._assert_return_code(result)

    bec_inhibit_inputs_2 = ['lck', 'fal', 'na']

    @slash.parametrize('edhs', bec_inhibit_inputs_2)
    def test_bec_inhibit_mode_2(self, edhs):
        """
        Run Test - test_bec_inhibit_mode_2
        https://ford.atlassian.net/browse/ZOPRO-26906
        """

        result = self.execute_vlab_test("test_bec_inhibit_mode_2", inputs=edhs)
        self._assert_return_code(result)

    fec_inhibit_inputs = [
        ('bec', 'ajar'),
        ('bec', 'clsd'),
        ('bec', 'fal'),
        ('bec', 'unk'),
        ('bec', 'na'),
    ]

    @slash.parametrize(('drid', 'das'), common_inhibit_inp + fec_inhibit_inputs)
    def test_fec_inhibit_mode(self, drid, das):
        """
        Run Test - test_fec_inhibit_mode
        https://ford.atlassian.net/browse/ZOPRO-26905
        """

        result = self.execute_vlab_test("test_fec_inhibit_mode", inputs=f"{drid}::{das}")
        self._assert_return_code(result)

    fec_inhibit_inputs_2 = ['lck', 'fal', 'na']

    @slash.parametrize('edhs', fec_inhibit_inputs_2)
    def test_fec_inhibit_mode_2(self, edhs):
        """
        Run Test - test_fec_inhibit_mode_2
        https://ford.atlassian.net/browse/ZOPRO-26905
        """

        result = self.execute_vlab_test("test_fec_inhibit_mode_2", inputs=edhs)
        self._assert_return_code(result)
