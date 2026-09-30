import time
import datetime
import sys
import argparse, textwrap
import vlab
import can
import sim_logger

logger = sim_logger.logger

# setup info
FIM_COMP_NAME = "fim_zonal"
FIM_NODE_ID = 3
SYNC_DELAY = 1


def connect_ports():
    logger.debug("[{}] : connect vlab ports".format(FIM_COMP_NAME))

    def connect_systemc_fim_eth_port():
        vlab.connect(("RH850", "ETNB0_TX"), (FIM_COMP_NAME, "ETH_RX"))
        vlab.connect((FIM_COMP_NAME, "ETH_TX"), ("RH850", "ETNB0_RX"))

    def connect_systemc_cantoken_busrouter():
        can_bus_t = vlab.component(name="CANTokenBusRouter", module="can.CANTokenBusRouter")
        vlab.instantiate(can_bus_t, "CANBUS0", args=[vlab.NAME, 2])  # two connections
        vlab.connect(vlab.STUB, ("CANBUS0", "RESETN"), default=True)
        vlab.connect(vlab.STUB, ("CANBUS0", "RESET"), default=False)

    def connect_systemc_fim_cantoken_ctrl():
        vlab.connect((FIM_COMP_NAME, "CAN_TOKEN_TX_CTRL"), ("CANBUS0", "IN_TX_CTRL", 0))
        vlab.connect(("RH850", "RSCAN0_TOKEN_TX_CTRL1"), ("CANBUS0", "IN_TX_CTRL", 1))
        vlab.connect(
            ("CANBUS0", "OUT_RX_CTRL"),
            [(FIM_COMP_NAME, "CAN_TOKEN_RX_CTRL"), ("RH850", "RSCAN0_TOKEN_RX_CTRL1")],
        )

    def connect_systemc_fim_cantoken_data():
        vlab.connect((FIM_COMP_NAME, "CAN_TOKEN_TX_DATA"), ("CANBUS0", "IN_TX_DATA", 0))
        vlab.connect(("RH850", "RSCAN0_TOKEN_TX_DATA1"), ("CANBUS0", "IN_TX_DATA", 1))
        vlab.connect(
            ("CANBUS0", "OUT_RX_DATA"),
            [(FIM_COMP_NAME, "CAN_TOKEN_RX_DATA"), ("RH850", "RSCAN0_TOKEN_RX_DATA1")],
        )

    connect_systemc_fim_eth_port()
    connect_systemc_cantoken_busrouter()
    connect_systemc_fim_cantoken_ctrl()
    connect_systemc_fim_cantoken_data()
    vlab.write_attribute("RH850.PFRH850.RSCAN0.ENGINE", "token")


def testbench_main():
    logger.info("==============================================================================")
    logger.info("FordSIM - FIM Zonal Testbench [node {}]".format(FIM_NODE_ID))
    logger.info("==============================================================================")

    logger.debug("FIM: setup connection")

    # instantiate fim component and specify the number of GPIO ports
    fim_comp = vlab.component("fim", module="fim")
    fim_inst = vlab.instantiate(fim_comp, FIM_COMP_NAME, args=[vlab.NAME, 64])

    # Optional remappings of GPIO numbers received over MQTT to the
    # internal fim pin numbers.
    # fim_inst.obj.add_gpio_mapping(1, 3)

    # instantiate fim network node
    # Refer to 'fim_vlab_python_api.hpp' for default values
    fim_node_inst = fim_inst.obj.get_fordsim_node()
    # fim_node_inst.set_nodeid(FIM_NODE_ID)
    # fim_node_inst.set_conn_client_name(FIM_COMP_NAME)
    #
    # # connect to fordsim mqtt bus
    # fim_node_inst.setup_conn()
    # fim_node_inst.connect()
    #
    # # subscribe to fim - mqtt/CAN peripheral bus
    # fim_node_inst.subscribe_can()
    #
    # # subscribe to fim - mqtt/ETH peripheral bus
    # fim_node_inst.subscribe_eth()
    #
    # # subscribe to fim - mqtt/CSI peripheral bus
    # fim_node_inst.subscribe_csi()
    #
    # # subscribe to fim - mqtt/SPI peripheral bus
    # fim_node_inst.subscribe_spi()
    #
    # # subscribe to fim - mqtt/PSI5 peripheral bus
    # fim_node_inst.subscribe_psi5()
    #
    # # subscribe to fim - mqtt/GPIO peripheral bus
    # fim_node_inst.subscribe_gpio()

    connect_ports()

    # there should be no unconnected ports, but if there are any,
    # we can just stub them out.
    vlab.stub(fim_inst)


try:
    logger.info(
        "[{}] testbench option : nodeid [{}] : syncdelay [{}]".format(
            FIM_COMP_NAME, FIM_NODE_ID, SYNC_DELAY
        )
    )

    # vecu synchronize delay
    time.sleep(int(SYNC_DELAY))

    testbench_main()

except Exception as e:
    logger.exception("[{}] testbench failed to load error [{}]".format(FIM_COMP_NAME, str(e)))
    raise
