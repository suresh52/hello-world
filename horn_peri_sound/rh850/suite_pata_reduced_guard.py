import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, ReducedGuard, VehPwMdeStat)


class ReduceGuard(VlabTestCase):
    """
    This class holds the test case for PATA - ReducedGuard Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(ReduceGuard, self).before(args)
        self.initialize()

    def after(self, args):
        super(ReduceGuard, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_reduced_guard_on(self, args):
        """
        This is to test ReducedGuard on/off:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26901
        """
        reducedguard = args.inputs
        reducedguard_stat = args.outputs
        reducedguard_val = ReducedGuard.from_str(reducedguard)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step("Set ReducedGuardDreq  = {}".format(reducedguard_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val", reducedguard_val, 'uint8')
        self.call_10ms_runnable_multiple_times()

        result = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDStat_Val", 'uint8')

        if reducedguard_stat == 'persis':
            self.verify_equal(result, ReducedGuard.ReducedGuard_PERSISTENTON)
        elif reducedguard_stat == 'on':
            self.verify_equal(result, ReducedGuard.ReducedGuard_ON)
        else:
            self.verify_equal(result, ReducedGuard.ReducedGuard_OFF)

    def test_reduced_guard_off(self, args):
        """
        This is to test the Reduced Guard off:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22312
        """

        self.step("setting reduced guard on")
        self.set_reduced_guard_on()
        self.step("Set ReducedGuardDreq  = off")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val",
                          ReducedGuard.ReducedGuard_OFF, 'uint8')
        self.call_10ms_runnable_multiple_times()

        result = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDStat_Val", 'uint8')
        self.verify_equal(result, ReducedGuard.ReducedGuard_OFF)

    def test_reduced_guard_off_with_vehpwrmode(self, args):
        """
        This is to test the Reduced Guard off:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22312
        """

        (vehpwmde, reduced_guard) = args.inputs.split("::")
        vehpwmde_val = VehPwMdeStat.from_str(vehpwmde)
        self.step("setting reduced guard on")
        self.set_reduced_guard_on()
        self.step("Set VehPwMde  = {}".format(vehpwmde_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_VehPwMdeStat_Grp", vehpwmde_val, 'uint8')
        self.call_10ms_runnable_multiple_times()

        result = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDStat_Val", 'uint8')
        if reduced_guard == "off":
            self.verify_equal(result, ReducedGuard.ReducedGuard_OFF)
        else:
            self.verify_equal(result, ReducedGuard.ReducedGuard_ON)
