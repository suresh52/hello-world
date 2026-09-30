from enum import IntEnum

invalid_str_value = "The given value {} is invalid"


class SosPostCrashSts(IntEnum):
    """
    SOSPostCrashSts ENUMs
    """

    FALSE = 0
    TRUE = 1

    @staticmethod
    def from_str(name):  # noqa
        try:
            return SosPostCrashSts[name.upper()]
        except KeyError:
            return invalid_str_value.format(name)


class PostCrashSts(IntEnum):
    """
    PostCrashSts ENUMs
    """

    FALSE = 0
    TRUE = 1


class CrashEvntDStat(IntEnum):
    """
    CrashEvntDStat ENUMs
    """

    NO_EVENT = 0
    DEPLOY_EVENT = 1
    FUEL_CUTOFF_EVENT = 2
    INVALID = 3

    @staticmethod
    def from_str(name):  # noqa
        try:
            return CrashEvntDStat[name.upper()]
        except KeyError:
            return invalid_str_value.format(name)


class UseCaseNumber:
    """
    USECASE Id value
    """
    CRASH_EVENT_OCCURRENCE = 1587609467


class CommonStrings:
    """
    Common Strings used in the scripts
    """

    setting_sos_post_crash_sts = "Setting SosPostCrashsts "
    setting_crash_evnt_d_stat_str = "Setting CrashEvntDStat "
    sos_post_crash_sts_variable = "SOSPostCrashAlert_NvmSOSPostCrashSts"
    post_crash_sts_variable = "Rte_SOSPostCrashAlert_SOSPostCrashSts_PostCrashSts"
    crash_event_d_stat_variable = "Rte_SOSPostCrashAlert_CrashEvntDStat_Val"
    usecase_id_variable = "SOSPostCrashAlert_ResourceManagerDirect_startUseCase_useCaseId"
