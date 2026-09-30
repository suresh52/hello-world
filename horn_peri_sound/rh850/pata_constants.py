from enum import IntEnum

invalid_str_value = "The given value {} is invalid"


class PerimeterAlarmCfgM2(IntEnum):
    """
    PerimeterAlarmCfgM2 ENUMs
    """
    ENABLED = 1
    DISABLED = 0

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "enbl":
            return PerimeterAlarmCfgM2.ENABLED
        elif name == "disbl":
            return PerimeterAlarmCfgM2.DISABLED
        raise ValueError(invalid_str_value.format(name))


class VehPwMdeStat(IntEnum):
    """
    VehPwMdeStat ENUMs
    """
    NOT_USED1 = 0
    VPM10 = 1
    VPM20 = 2
    NOT_USED2 = 3
    VPM40 = 4
    VPM50 = 5
    VPM60 = 6
    VPM70 = 7

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "nu1":
            return VehPwMdeStat.NOT_USED1
        elif name == "vpm10":
            return VehPwMdeStat.VPM10
        elif name == "vpm20":
            return VehPwMdeStat.VPM20
        elif name == "nu2":
            return VehPwMdeStat.NOT_USED2
        elif name == "vpm40":
            return VehPwMdeStat.VPM40
        elif name == "vpm50":
            return VehPwMdeStat.VPM50
        elif name == "vpm60":
            return VehPwMdeStat.VPM60
        elif name == "vpm70":
            return VehPwMdeStat.VPM70
        raise ValueError(invalid_str_value.format(name))


class LifeCycMdeDActl(IntEnum):
    """
    LifeCycMdeDActl ENUMs
    """
    NORMAL = 0
    FACTORYFINISH = 1
    NOTUSED2 = 2
    TRANSPORT = 3
    NOTUSED4 = 4
    RECOMDECOM = 5
    NOTUSED6 = 6
    FACTORYINPLANTFLASH = 7
    FACTORYTESTSTATION = 8
    FACTORYTRANSITION = 9
    NOTUSED10 = 10
    NOTUSED11 = 11
    NOTUSED12 = 12
    NOTUSED13 = 13
    NOTUSED14 = 14
    NOTUSED15 = 15

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "nrml":
            return LifeCycMdeDActl.NORMAL
        elif name == "ff":
            return LifeCycMdeDActl.FACTORYFINISH
        elif name == "nu_2":
            return LifeCycMdeDActl.NOTUSED2
        elif name == "tprt":
            return LifeCycMdeDActl.TRANSPORT
        elif name == "nu_4":
            return LifeCycMdeDActl.NOTUSED4
        elif name == "rcm":
            return LifeCycMdeDActl.RECOMDECOM
        elif name == "nu_6":
            return LifeCycMdeDActl.NOTUSED6
        elif name == "fif":
            return LifeCycMdeDActl.FACTORYINPLANTFLASH
        elif name == "fts":
            return LifeCycMdeDActl.FACTORYTESTSTATION
        elif name == "ft":
            return LifeCycMdeDActl.FACTORYTRANSITION
        elif name == "nu10":
            return LifeCycMdeDActl.NOTUSED10
        elif name == "nu11":
            return LifeCycMdeDActl.NOTUSED11
        elif name == "nu12":
            return LifeCycMdeDActl.NOTUSED12
        elif name == "nu13":
            return LifeCycMdeDActl.NOTUSED13
        elif name == "nu14":
            return LifeCycMdeDActl.NOTUSED14
        elif name == "nu15":
            return LifeCycMdeDActl.NOTUSED15
        raise ValueError(invalid_str_value.format(name))


class OnChangeInfiniteTimerStatus(IntEnum):
    """
    OnChangeInfiniteTimerStatus ENUMs
    """
    RequestStatusType_DEFAULT = 0
    RequestStatusType_CONFIRMED = 1
    RequestStatusType_REJECTED = 2
    RequestStatusType_ERROR = 3

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "def":
            return OnChangeInfiniteTimerStatus.RequestStatusType_DEFAULT
        elif name == "cnf":
            return OnChangeInfiniteTimerStatus.RequestStatusType_CONFIRMED
        elif name == "rej":
            return OnChangeInfiniteTimerStatus.RequestStatusType_REJECTED
        elif name == "err":
            return OnChangeInfiniteTimerStatus.RequestStatusType_ERROR
        raise ValueError(invalid_str_value.format(name))


class ExteriorVehicleLockStatus(IntEnum):
    """
    ExteriorVehicleLockStatus ENUMs
    """
    CENTRALLY_LOCKED = 0
    CENTRALLY_UNLOCKED = 1
    PARTIALLY_LOCKED = 2

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "cen_lck":
            return ExteriorVehicleLockStatus.CENTRALLY_LOCKED
        elif name == "par_lck":
            return ExteriorVehicleLockStatus.PARTIALLY_LOCKED
        elif name == "cen_unlck":
            return ExteriorVehicleLockStatus.CENTRALLY_UNLOCKED
        raise ValueError(invalid_str_value.format(name))


class ExteriorLockEventCount(IntEnum):
    """
    ExteriorLockEventCount values
    """

    VALUE_0 = 0
    VALUE_1 = 1

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "val0":
            return ExteriorLockEventCount.VALUE_0
        elif name == "val1":
            return ExteriorLockEventCount.VALUE_1
        raise ValueError(invalid_str_value.format(name))


class LastLockUnlockRequestor(IntEnum):
    """
    LastLockUnlockRequestor ENUMs
    """
    INTERIOR = 0
    EXTERIOR = 1
    CELLULAR = 2
    REMOTE = 3
    EMERGENCY = 4
    WITHOUT_REQUEST = 5

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "int":
            return LastLockUnlockRequestor.INTERIOR
        elif name == "ext":
            return LastLockUnlockRequestor.EXTERIOR
        elif name == "cell":
            return LastLockUnlockRequestor.CELLULAR
        elif name == "rem":
            return LastLockUnlockRequestor.REMOTE
        elif name == "eme":
            return LastLockUnlockRequestor.EMERGENCY
        elif name == "wo_req":
            return LastLockUnlockRequestor.WITHOUT_REQUEST
        raise ValueError(invalid_str_value.format(name))


class PerimeterAlrmStat(IntEnum):
    """
    PerimeterAlrmStat ENUMs
    """
    PerimeterAlrmStat_DISARMED = 0
    PerimeterAlrmStat_PREARMED = 1
    PerimeterAlrmStat_ARMED = 2
    PerimeterAlrmStat_ACTIVATED = 3


class DrAjarStatus(IntEnum):
    """
    DoorAjarStatus ENUMs
    """
    CLOSED = 0
    AJAR = 1
    FAULTY = 2
    UNKNOWN = 3
    NOT_AVAILABLE = 4

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "clsd":
            return DrAjarStatus.CLOSED
        elif name == "ajar":
            return DrAjarStatus.AJAR
        elif name == "fal":
            return DrAjarStatus.FAULTY
        elif name == "unk":
            return DrAjarStatus.UNKNOWN
        elif name == "na":
            return DrAjarStatus.NOT_AVAILABLE
        raise ValueError(invalid_str_value.format(name))


class SensorTriggeredData(IntEnum):
    """
    SensorTriggeredData ENUMs
    """
    SensorTriggeredDataEnum_TRIGGERED = 0
    SensorTriggeredDataEnum_NOT_TRIGGERED = 1

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "trig":
            return SensorTriggeredData.SensorTriggeredDataEnum_TRIGGERED
        elif name == "not_trig":
            return SensorTriggeredData.SensorTriggeredDataEnum_NOT_TRIGGERED
        raise ValueError(invalid_str_value.format(name))


class DrID(IntEnum):
    """
    Door index value
    """
    DRIVER_DOOR = 0
    PASSENGER_DOOR = 1
    DRIVER_SECOND_ROW_DOOR = 2
    PASSENGER_SECOND_ROW_DOOR = 3
    BEC_ENCLOSURE = 4
    BEC2_ENCLOSURE = 5
    FEC_ENCLOSURE = 6
    DRIVER_THIRD_ROW_DOOR = 7
    PASSENGER_THIRD_ROW_DOOR = 8
    BEC3_ENCLOSURE = 9

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "df":
            return DrID.DRIVER_DOOR
        elif name == "pf":
            return DrID.PASSENGER_DOOR
        elif name == "dr":
            return DrID.DRIVER_SECOND_ROW_DOOR
        elif name == "pr":
            return DrID.PASSENGER_SECOND_ROW_DOOR
        elif name == "bec":
            return DrID.BEC_ENCLOSURE
        elif name == "bec2":
            return DrID.BEC2_ENCLOSURE
        elif name == "fec":
            return DrID.FEC_ENCLOSURE
        elif name == "dtr":
            return DrID.DRIVER_THIRD_ROW_DOOR
        elif name == "ptr":
            return DrID.PASSENGER_THIRD_ROW_DOOR
        elif name == "bec3":
            return DrID.BEC3_ENCLOSURE
        raise ValueError(invalid_str_value.format(name))


class Timer(IntEnum):
    """
    These are the constants used in the script
    """
    INITIAL_TIMER = 0
    ARMING_DELAY_TIMER = 20


class SecurityCfgM2(IntEnum):
    """
    SecurityCfgM2 ENUMs
    """
    SECURITYCFG_NONE = 0
    SECURITYCFG_BOTH = 1
    SECURITYCFG_INCLINATION = 2
    SECURITYCFG_INTRUSION = 3
    SECURITYCFG_INTRUSION_REAR_INTRUSION = 4
    SECURITYCFG_BOTH_REAR_INTRUSION = 5

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "none":
            return SecurityCfgM2.SECURITYCFG_NONE
        elif name == "bth":
            return SecurityCfgM2.SECURITYCFG_BOTH
        elif name == "incli":
            return SecurityCfgM2.SECURITYCFG_INCLINATION
        elif name == "intru":
            return SecurityCfgM2.SECURITYCFG_INTRUSION
        elif name == "iri":
            return SecurityCfgM2.SECURITYCFG_INTRUSION_REAR_INTRUSION
        elif name == "bri":
            return SecurityCfgM2.SECURITYCFG_BOTH_REAR_INTRUSION
        raise ValueError(invalid_str_value.format(name))


class ExteriorDoorHandleStatus(IntEnum):
    """
    ExteriorDoorHandleStatus ENUMs
    """
    ExteriorDoorHandleStatus_LOCKED = 0
    ExteriorDoorHandleStatus_UNLOCKED = 1
    ExteriorDoorHandleStatus_LOCK_STATUS_NOT_AVAILABLE = 2
    ExteriorDoorHandleStatus_LOCK_STATUS_FAULTY = 3

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "lck":
            return ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_LOCKED
        elif name == "unlck":
            return ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_UNLOCKED
        elif name == "na":
            return ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_LOCK_STATUS_NOT_AVAILABLE
        elif name == "fal":
            return ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_LOCK_STATUS_FAULTY
        raise ValueError(invalid_str_value.format(name))


class SensorState(IntEnum):
    """
    SensorState ENUMs
    """
    SensorStateEnum_ARMED = 0
    SensorStateEnum_DISARMED = 1
    SensorStateEnum_UNKNOWN = 2

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "arm":
            return SensorState.SensorStateEnum_ARMED
        elif name == "disarm":
            return SensorState.SensorStateEnum_DISARMED
        elif name == "unk":
            return SensorState.SensorStateEnum_UNKNOWN
        raise ValueError(invalid_str_value.format(name))


class ReducedGuard(IntEnum):
    """
    ReducedGuard ENUMs
    """
    ReducedGuard_NULL = 0
    ReducedGuard_OFF = 1
    ReducedGuard_ON = 2
    ReducedGuard_PERSISTENTON = 3

    @staticmethod  # noqa
    def from_str(name):  # noqa
        name = name.lower()
        if name == "null":
            return ReducedGuard.ReducedGuard_NULL
        elif name == "off":
            return ReducedGuard.ReducedGuard_OFF
        elif name == "on":
            return ReducedGuard.ReducedGuard_ON
        elif name == "persis":
            return ReducedGuard.ReducedGuard_PERSISTENTON
        raise ValueError(invalid_str_value.format(name))


class TrailerConnectCfgM2(IntEnum):
    """
    TrailerConnectCfgM2 ENUMs
    """
    DISABLED = 0
    ENABLED = 1

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "enbl":
            return TrailerConnectCfgM2.ENABLED
        elif name == "disbl":
            return TrailerConnectCfgM2.DISABLED
        raise ValueError(invalid_str_value.format(name))


class OnChangeTrailerAlarmSetting(IntEnum):
    """
    OnChangeTrailerAlarmSetting ENUMs
    """
    TrailerConnectionAlarmSetting_OFF = 0
    TrailerConnectionAlarmSetting_ON = 1

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "off":
            return OnChangeTrailerAlarmSetting.TrailerConnectionAlarmSetting_OFF
        elif name == "on":
            return OnChangeTrailerAlarmSetting.TrailerConnectionAlarmSetting_ON
        raise ValueError(invalid_str_value.format(name))


class TrailerConnection(IntEnum):
    """
    Trailer Connection ENUMs
    """
    TrailerConnection_TRAILER_CONNECTION_NO = 0
    TrailerConnection_TRAILER_CONNECTION_YES = 1

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "no":
            return TrailerConnection.TrailerConnection_TRAILER_CONNECTION_NO
        elif name == "yes":
            return TrailerConnection.TrailerConnection_TRAILER_CONNECTION_YES
        raise ValueError(invalid_str_value.format(name))


class TrailerAlarmActivation(IntEnum):
    """
    Trailer Alarm Activation ENUMs
    """
    TrailerAlarmActivation_TRAILER_ALARM_INACTIVE = 0
    TrailerAlarmActivation_TRAILER_ALARM_ACTIVE = 1


class OnChangeTrailerAlarmTimer(IntEnum):
    """
    Trailer Alarm Timer ENUMs
    """
    RUN = 0
    END = 1

    @staticmethod
    def from_str(name):  # noqa
        name = name.lower()
        if name == "run":
            return OnChangeTrailerAlarmTimer.RUN
        elif name == "end":
            return OnChangeTrailerAlarmTimer.END
        raise ValueError(invalid_str_value.format(name))


class WarningLightRequest(IntEnum):
    """
    Warning Light Request ENUMs
    """
    OFF = 0
    ON = 1


class SounderPattern(IntEnum):
    """
    SounderPattern ENUMs
    """
    CHIRP_1 = 0
    CHIRP_2 = 1
    CHIRP_3 = 2
    CHIRPHONK = 3
    CHIRP_2H = 4
    BEEP_1 = 5
    BEEP_2 = 6
    BEEP = 7
    BEEP_OOA = 8
    PERIMETER_ALARM1_H = 9
    PERIMETER_ALARM2_H = 10
    PERIMETER_ALARM1_SH = 11
    PERIMETER_ALARM2_SH = 12
    PERIMETER_ALARM1_BBS = 13
    PERIMETER_ARMBBS = 14
    PERIMETER_ALARM1_H_BBS = 15
    PERIMETER_ALARM2_H_BBS = 16
    HONK = 17
    POST_CRASH = 18
    PANIC_ALARM_1 = 19
    PANIC_ALARM_2 = 20


class SoundRequest(IntEnum):
    """
    Sound Request ENUMs
    """
    DEACTIVATE = 0
    ACTIVATE = 1


class PauseBetweenRepetition(IntEnum):
    """
    Pause Between Repetition Default value
    """
    DEFAULT_VALUE = 0


class ActivationTimeStamp(IntEnum):
    """
    Activation Time Stamp default value
    """
    DEFAULT_VALUE = 0


class REPETITION(IntEnum):
    """
    Activation Time Stamp default value
    """
    DEFAULT_VALUE = 0


class UseCaseNumber(IntEnum):
    """
    UseCaseNumber Fixed values for Prearmed, Armed and Activated
    """
    PREARMED_ARMED = 2527034385
    ACTIVATED = 2320116114


class HornSoundCfgM2(IntEnum):
    """
    HornSoundCfgM2 ENUMs
    """
    OFF = 0
    ON = 1


class PrmtrAlrmEvntDStat(IntEnum):
    """
    PrmtrAlrmEvntDStat ENUMs
    """
    NULL = 0
    DF_DOOR = 1
    PF_DOOR = 2
    DR_DOOR = 3
    PR_DOOR = 4
    LG_DOOR = 5
    CARGO_DR = 6  # CARGO_DOOR
    DECKLID = 7
    HOOD = 8
    INCLI = 9  # INCLINATION
    INTRU = 10  # INTRUSION
    R_INTRU = 11  # REAR_INTRUSION
    TRAILER = 12
    DIAGTMPR = 13  # DIAG_TAMPER

    @staticmethod
    def from_str(name):  # noqa
        try:
            return PrmtrAlrmEvntDStat[name.upper()]
        except KeyError:
            return invalid_str_value.format(name)


class AlarmSoundCfgM2(IntEnum):
    """
    AlarmSoundCfgM2 ENUMs
    """
    VEHICLE_HORN = 0
    SECURITY_HORN = 1
    BBS = 2
    BBS_VEHICLE_HORN = 3

    @staticmethod
    def from_str(name):  # noqa
        try:
            return AlarmSoundCfgM2[name.upper()]
        except KeyError:
            return invalid_str_value.format(name)


class CommonStrings:
    """
    Common strings used in scripts.
    """
    setting_armed_mode_str = "Setting the alarm status to ARMED"
    setting_activated_mode_str = "setting the alarm to activated"
    setting_prearmed_mode_str = "Setting the alarm status to PREARMED"
    setting_partially_locked_str = "Setting exteriorVehicleLockStatus= PARTIALLY_LOCKED"
    checking_alarm_status_str = "Checking the alarm status"
    door_ajar_status_variable = "Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[{}]"
    setting_doorajarstatus_str = "Set doorAjarStatus[{}] = {}"
    setting_trailer_alarm_armed_str = "set trailer alarm armed"
    checking_trailer_alarm_str = "checking the trailer Alarm state"
    ext_door_handle_variable = ("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                                "exteriorDoorHandleStatus[{}]")
    intru_sensor_state_var = ("  Rte_PerimeterAlrmVehMdeNewTrgEvnt_intrusionStatusInterface_intrusionStatus"
                              ".SensorState")
    incli_sensor_state_var = ("  Rte_PerimeterAlrmVehMdeNewTrgEvnt_inclinationStatusInterface_inclinationStatus"
                              ".SensorState")
    intru_sensor_trig_data_var = ("Rte_PerimeterAlrmVehMdeNewTrgEvnt_intrusionStatusInterface_intrusionStatus"
                                  ".SensorTriggeredData")
    incli_sensor_trig_data_var = ("Rte_PerimeterAlrmVehMdeNewTrgEvnt_inclinationStatusInterface_inclinationStatus"
                                  ".SensorTriggeredData")
    setting_intrusion_armed_str = "Set intrusion trigger to armed"
    setting_inclination_armed_str = "set inclination trigger to armed"
    setting_intrusion_triggered_str = "Set intrusionStatus.SensorTriggeredData = Triggered"
    climate_airflow_lvl_var = ("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_climateAirflwSettingInterface_onChange_"
                               "climateAirflwSetting[18].ClimtAirFlowLvl")
    usecase_id_verification_str = "Verify the usecase number sent to the vehicle power state manager"
    usecase_id_variable = "PerimeterAlrmVehMdeNewTrgEvnt_ResourceManagerDirect_startUseCase_useCaseId"
    verify_warninglightrequest_str = "Verify the WarningLightRequest"
    verify_soundrequest_str = "Verify the soundRequest"
