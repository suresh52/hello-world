
import os
import software_utils_rh850 as utility

test_buffer_len_max = 1524*1
core = utility.CORE0

class fordsim_testbench_rh850:

    def __init__(self, vlab, fsim_py_testbench_read_test_output):
        self.vlab = vlab
        self.address_test_out = self.symbol_address('fsim_python_test_out')
        self.address_test_id = self.symbol_address('fsim_python_test_id')
        self.address_test_buffer_in = self.symbol_address('fsim_python_test_buffer_in')
        self.address_test_buffer_in_len = self.symbol_address('fsim_python_test_buffer_in_len')
        self.address_test_buffer_out = self.symbol_address('fsim_python_test_buffer_out')
        self.address_test_buffer_out_len = self.symbol_address('fsim_python_test_buffer_out_len')
        self.address_test_loging = self.symbol_address('fsim_python_test_log_buffer')
        self.address_test_loging_len = self.symbol_address('fsim_python_test_log_buffer_len')
        self.test_is_run = 0
        self.test_set_testid = -1
        self.test_set_buffer_in  = bytearray(test_buffer_len_max)
        self.vlab.add_software_stub("fsim_python_testbench_event2python_set_test_parameters", self.fsim_py_testbench_event_set_test_parameter)
        self.vlab.add_software_stub("fsim_python_testbench_event2python_get_test_result", self.fsim_py_testbench_event_get_test_result)
        self.fsim_py_testbench_read_test_output = fsim_py_testbench_read_test_output

    def symbol_address(self, symbol_name):
        symbol = self.vlab.get_symbols(name=symbol_name)
        addr = symbol[0].address
        return addr

    def symbol_size(self, symbol_name):
        symbol = self.vlab.get_symbols(name=symbol_name)
        if len(symbol) > 0:
            size = symbol[0].size
        else:
            size = symbol.size
        return size

    def fsim_py_testbench_execute_test( self, testId ,  buffer_in  )  :
        if (len(buffer_in) ==0 | len(buffer_in) > test_buffer_len_max | testId < 0 | testId > 0xFFFFFFFF):
            print('FSTB : Error : wrong an input argument.')
            return -1
        self.test_set_testid = testId
        self.test_set_buffer_in = buffer_in
        self.test_is_run = 1
        return 0

    def fsim_py_testbench_test_cleanup(self):
        self.test_is_run = 0
        self.test_set_testid = -1
        utility.vlab_set_int32(self.address_test_id, int(-1))

    def fsim_py_testbench_event_set_test_parameter(self):
        print('[{0}] : FSTB : set_test_parameter : {1}'.format(self.vlab.simulation_time(), self.test_set_testid))
        utility.vlab_set_int32(self.address_test_id, self.test_set_testid)
        utility.vlab_set_int32(self.address_test_buffer_in_len, len(self.test_set_buffer_in))
        self.vlab.write_memory(self.address_test_buffer_in, self.test_set_buffer_in, core=core)
        self.test_is_run = 2

    def fsim_py_testbench_event_get_test_result(self):
        print('[{0}] : FSTB : fsim_py_testbench_event_get_test_result : {1}'.format(self.vlab.simulation_time(), self.test_set_testid))

        test_out = utility.vlab_get_int32(self.address_test_out)
        buffer_out_len = utility.vlab_get_int32(self.address_test_buffer_out_len)
        buffer_out = bytearray()
        if (buffer_out_len < 0 or buffer_out_len > test_buffer_len_max):
            print('FSTB : wrong buffer_out_len: {0}'.format(buffer_out_len))
        else :
            buffer_out = self.vlab.read_memory(self.address_test_buffer_out, buffer_out_len, core=core)

        loging_len = utility.vlab_get_int32(self.address_test_loging_len)
        test_loging = bytearray()
        if (loging_len < 0 | loging_len > test_buffer_len_max):
            print('FSTB : wrong loging_len: {0}'.format(loging_len))
        else:
            test_loging = self.vlab.read_memory(self.address_test_loging, loging_len,  core=core)
        self.fsim_py_testbench_read_test_output(self.test_set_testid, test_out, buffer_out, test_loging)
        
