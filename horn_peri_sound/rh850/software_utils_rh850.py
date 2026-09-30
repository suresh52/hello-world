""" This file should contain all the common function which will be used
in the test cases.
"""
import vlab


CORE0 = "RH850.CPUSS.PE0_FastIss"
PACK_FMT = {
    'int8':    "b",
    'uint8':   "B",
    'int16':   "h",
    'uint16':  "H",
    'int32':   "i",
    'uint32':  "I",
    'boolean': "?",
}


# TODO: revisit this function
def symbol_address(symbol_name):
    symbol = vlab.get_symbols(name=symbol_name)
    addr = symbol[0].address
    return addr


# TODO: revisit this function
def read_symbol_memory(symbol_name, length):
    address = symbol_address(symbol_name)
    return bytes(vlab.read_memory(address, size=length, core=CORE0, unpack='<i'))


class VlabMemory:

    def __init__(self, byte_order='<'):
        """This class contains API call to write and read the memory of Vlab."""
        self.byte_order = byte_order

    def write(self, address, data, fmt):
        """Function to write to a give address or symbol expression with the specified data
        this function will map the given data into the specified format.

        :param address: Address or Symbol expression
        :type address:  str
        :param data:    Data to be set at the memory
        :type data:     int or [int]
        :param fmt:     Data to be packed into, for struct packing list of str can be givem
        :type fmt:      str or [str]
        """
        if not isinstance(fmt, list):
            fmt = [fmt]
        fmt = self._encode_pack_fmt(fmt)

        if not isinstance(data, list):
            data = [data]

        if len(data) != len(fmt):
            raise ValueError("Given data and format lengths must be same, but got {}, {}".format(len(data), len(fmt)))

        fmt = "".join(fmt)
        vlab.write_memory(address, data, core=CORE0, pack='{}{}'.format(self.byte_order, fmt))

    def read(self, address, fmt):
        """Function to read to a give address or symbol expression and will unpack it the specified
        format.

        :param address: Address or Symbol expression
        :type address:  str
        :param fmt:     Data to be packed into, for struct packing list of str can be givem
        :type fmt:      str or [str]
        :return:        Read data at the specified location
        :rtype:         int or [int]
        """
        if not isinstance(fmt, list):
            fmt = [fmt]

        fmt = self._encode_pack_fmt(fmt)
        fmt = "".join(fmt)
        return vlab.read_memory(address, core=CORE0, unpack='{}{}'.format(self.byte_order, fmt))

    def _encode_pack_fmt(self, fmts):
        _fmt = []
        for fmt in fmts:
            fmt = fmt.lower()
            if fmt not in PACK_FMT:
                raise ValueError("Given format is invalid = {}, possible values"
                                 " are {}".format(fmt, PACK_FMT.keys()))
            _fmt.append(PACK_FMT[fmt])
        return _fmt
