import unittest
from collections import OrderedDict
import filecmp

from file_utilities import readCSVFile, writeCSVFile, \
  fileMatchingRegexStringExists, getFileNamesMatchingRegexString


class FileUtilitiesTester(unittest.TestCase):

  def setUp(self):
    pass

  def testReadCSVData(self):
    input_file = "testing/tests/file_utilities/gold/test_data.csv"
    data = readCSVFile(input_file)

    self.assertTrue(data["header2"][1] == 5)

  def testWriteCSVData(self):
    data = OrderedDict()
    data["header1"] = [1, 2, 3]
    data["header2"] = [4, 5, 6]
    path = "testing/tests/file_utilities/"
    output_file = path + "test_data.csv"
    gold_file = path + "gold/test_data.csv"
    writeCSVFile(data, output_file)

    self.assertTrue(filecmp.cmp(output_file, gold_file))

  def testFileMatchingRegexStringExists(self):
    regex_existent = "testing/tests/file_utilities/gold/test_.*\.csv"
    regex_nonexistent = "testing/tests/file_utilities/gold/foo_.*\.csv"

    self.assertTrue(fileMatchingRegexStringExists(regex_existent))
    self.assertFalse(fileMatchingRegexStringExists(regex_nonexistent))

  def testGetFileNamesMatchingRegexString(self):
    regex = "testing/tests/file_utilities/gold/test_.*\.csv"
    correct_filename = "testing/tests/file_utilities/gold/test_data.csv"

    self.assertTrue(getFileNamesMatchingRegexString(regex) == [correct_filename])
