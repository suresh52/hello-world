import vlab

from common import VlabTestCase
from sos_constants import (SosPostCrashSts, CommonStrings, CrashEvntDStat)


class CrashEventOccurrence(VlabTestCase):
    """
    This class holds the test case for SOS Post Crash Alert Event Occurrence.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "SOSPostCrashAlert.elf"

    def before(self, args):
        super(CrashEventOccurrence, self).before(args)
        self.initialize()

    def after(self, args):
        super(CrashEventOccurrence, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("SOSPostCrashAlert_Init ", blocking=True)

    def test_crash_event_occurrence_1(self, args):
        """
        This is to test SOS Crash Event Occurrence:
        https://ford.atlassian.net/browse/ZOPRO-28367
        """

        crash_event_stat = args.inputs
        crash_event_stat_val = CrashEvntDStat.from_str(crash_event_stat)

        self.step(CommonStrings.setting_sos_post_crash_sts + "to FALSE")
        self.memory.write(CommonStrings.sos_post_crash_sts_variable, SosPostCrashSts.FALSE, "boolean")
        self.call_10ms_sos_runnable()

        self.step(CommonStrings.setting_crash_evnt_d_stat_str + crash_event_stat)
        self.memory.write(CommonStrings.crash_event_d_stat_variable, crash_event_stat_val, "uint8")

        self.call_10ms_sos_runnable()

        pos_crash_sts_value = self.memory.read(CommonStrings.post_crash_sts_variable, 'boolean')
        sos_pos_crash_sts_value = self.memory.read(CommonStrings.sos_post_crash_sts_variable, 'boolean')
        usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')

        if crash_event_stat == "deploy_event":
            self.verify_crash_event_occurrence(pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value, True)

        elif crash_event_stat == "fuel_cutoff_event":
            self.verify_crash_event_occurrence(pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value, True)

        else:
            self.verify_crash_event_occurrence(pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value, False)

    def test_crash_event_occurrence_2(self, args):
        """
        This is to test SOS Crash Event Occurrence:
        https://ford.atlassian.net/browse/ZOPRO-28367
        """

        sos_pos_crash_sts = args.inputs
        sos_pos_crash_sts_val = SosPostCrashSts.from_str(sos_pos_crash_sts)

        self.step(CommonStrings.setting_sos_post_crash_sts + sos_pos_crash_sts)
        self.memory.write(CommonStrings.sos_post_crash_sts_variable, sos_pos_crash_sts_val, "boolean")

        self.call_10ms_sos_runnable(3)

        pos_crash_sts_value = self.memory.read(CommonStrings.post_crash_sts_variable, 'boolean')
        sos_pos_crash_sts_value = self.memory.read(CommonStrings.sos_post_crash_sts_variable, 'boolean')
        usecase_value = self.memory.read(CommonStrings.usecase_id_variable, 'uint32')

        if sos_pos_crash_sts == "true":
            self.verify_crash_event_occurrence(pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value, True)

        else:
            self.verify_crash_event_occurrence(pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value, False)
