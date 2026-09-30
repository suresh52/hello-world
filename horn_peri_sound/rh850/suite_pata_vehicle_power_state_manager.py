import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, UseCaseNumber)


class VehiclePowerStateManager(VlabTestCase):
    """
    This class holds the test case for PATA - Vehicle Power State Manager.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(VehiclePowerStateManager, self).before(args)
        self.initialize()

    def after(self, args):
        super(VehiclePowerStateManager, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_vehicle_power_state_manager(self, args):
        """
        This is to test the vehicle power state manager:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11359
        """
        alarmstat = args.inputs

        if alarmstat == "prearm":
            self.step(CommonStrings.setting_prearmed_mode_str)
            self.set_prearmed_mode()

            self.step(CommonStrings.usecase_id_verification_str)
            usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')
            self.verify_equal(usecase_value, UseCaseNumber.PREARMED_ARMED)

        elif alarmstat == "arm":
            self.step(CommonStrings.setting_armed_mode_str)
            self.set_armed_mode()

            self.step(CommonStrings.usecase_id_verification_str)
            usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')
            self.verify_equal(usecase_value, UseCaseNumber.PREARMED_ARMED)
        elif alarmstat == "act":
            self.step(CommonStrings.setting_activated_mode_str)
            self.set_activated_mode()

            self.step(CommonStrings.usecase_id_verification_str)
            usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')
            self.verify_equal(usecase_value, UseCaseNumber.ACTIVATED)

        else:
            self.step(CommonStrings.usecase_id_verification_str)
            usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')
            if usecase_value != UseCaseNumber.ACTIVATED or UseCaseNumber.PREARMED_ARMED:
                usecase_value = True
            self.verify_equal(usecase_value, True)
