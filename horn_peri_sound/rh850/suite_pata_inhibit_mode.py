import vlab

from common import VlabTestCase
from pata_constants import (DrAjarStatus, DrID, CommonStrings, ExteriorVehicleLockStatus, ExteriorDoorHandleStatus)


class InhibitMode(VlabTestCase):
    """
    This class holds the test case for PATA - Inhibit Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(InhibitMode, self).before(args)
        self.initialize()

    def after(self, args):
        super(InhibitMode, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_bec_inhibit_mode(self, args):
        """
        This is to test that the REAR ENCLOSURE Inhibit mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26906
        """

        (doorid, doorajarstatus) = args.inputs.split("::")
        doorid_val = DrID.from_str(doorid)
        doorajarstatus_val = DrAjarStatus.from_str(doorajarstatus)

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step(CommonStrings.setting_partially_locked_str)
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", ExteriorVehicleLockStatus.PARTIALLY_LOCKED, 'uint8')

        self.step("Set exteriorDoorHandleStatus[4] = UNLOCKED")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                          "exteriorDoorHandleStatus[4]", ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_UNLOCKED,
                          'uint8')
        self.call_10ms_runnable_multiple_times()

        self.step("Set doorAjarStatus[4] = {}".format(doorajarstatus_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[4]",
                          doorajarstatus_val, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step(CommonStrings.checking_alarm_status_str)
        self.verify_perimetere_alarm_armed()
        self.inhibit_state_verfication(doorid_val)

    def test_bec_inhibit_mode_2(self, args):
        """
        This is to test that the REAR ENCLOSURE Inhibit mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26906
        """

        ext_doorhandle_status = args.inputs
        ext_doorhandle_status_val = ExteriorDoorHandleStatus.from_str(ext_doorhandle_status)

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step(CommonStrings.setting_partially_locked_str)
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", ExteriorVehicleLockStatus.PARTIALLY_LOCKED, 'uint8')

        self.step("Set exteriorDoorHandleStatus[4] = {}".format(ext_doorhandle_status_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                          "exteriorDoorHandleStatus[4]", ext_doorhandle_status_val,
                          'uint8')

        self.step("Set doorAjarStatus[4] = AJAR")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[4]",
                          DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step(CommonStrings.checking_alarm_status_str)
        self.verify_perimetere_alarm_activated()

    def test_fec_inhibit_mode(self, args):
        """
        This is to test that the FRUNK Inhibit mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26905
        """

        (doorid, doorajarstatus) = args.inputs.split("::")
        doorid_val = DrID.from_str(doorid)
        doorajarstatus_val = DrAjarStatus.from_str(doorajarstatus)

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step(CommonStrings.setting_partially_locked_str)
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", ExteriorVehicleLockStatus.PARTIALLY_LOCKED, 'uint8')

        self.step("Set exteriorDoorHandleStatus[6] = UNLOCKED")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                          "exteriorDoorHandleStatus[6]", ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_UNLOCKED,
                          'uint8')
        self.call_10ms_runnable_multiple_times()
        self.step("Set doorAjarStatus[6] = {}".format(doorajarstatus_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[6]",
                          doorajarstatus_val, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step(CommonStrings.checking_alarm_status_str)
        self.verify_perimetere_alarm_armed()
        self.inhibit_state_verfication(doorid_val)

    def test_fec_inhibit_mode_2(self, args):
        """
        This is to test that the FRUNK Inhibit mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26905
        """

        ext_doorhandle_status = args.inputs
        ext_doorhandle_status_val = ExteriorDoorHandleStatus.from_str(ext_doorhandle_status)

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step(CommonStrings.setting_partially_locked_str)
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", ExteriorVehicleLockStatus.PARTIALLY_LOCKED, 'uint8')

        self.step("Set exteriorDoorHandleStatus[6] = {}".format(ext_doorhandle_status_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                          "exteriorDoorHandleStatus[6]", ext_doorhandle_status_val,
                          'uint8')

        self.step("Set doorAjarStatus[6] = AJAR")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[6]",
                          DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step(CommonStrings.checking_alarm_status_str)
        self.verify_perimetere_alarm_activated()
