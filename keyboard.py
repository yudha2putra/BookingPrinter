import unittest
import os
import sys
# import time
import logging

from escpos.connections import getUSBPrinter


class usbTest(unittest.TestCase):
    """
    To run these tests for BIXOLON USB printer set
        export PYTHON_ESCPOS_TEST_VENDORID=1504;
        export PYTHON_ESCPOS_TEST_PRODUCTID=0006;
        pyb run_unit_tests
    """

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger("USB.py tests")
        cls.log.debug("Initializing printer object")
        cls.USBPrinterClass = getUSBPrinter()
        cls.printer = cls.USBPrinterClass(idVendor=0x0483, idProduct=0x5840)

    def setUp(self):
        pass

    def test_setUp(cls):
        USBPrinterClass = getUSBPrinter(commandSet='Generic')
        printer = USBPrinterClass(idVendor=0x0483, idProduct=0x5840)
        cls.assertIsInstance(printer, USBPrinterClass)
        del printer

    def test__objIsInstance(cls):
        cls.assertIsInstance(cls.printer, cls.USBPrinterClass)

    def test_text(cls):
        cls.printer.text("TEST\n")

    def tearDown(self):
        pass  # time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        del cls.printer


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("USB.py tests").setLevel(logging.DEBUG)
    unittest.main()
