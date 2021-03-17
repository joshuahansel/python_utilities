import os
import numpy as np
import re
import csv


##
# Reads data from a CSV file
#
# @param[in] inputfile   Name of the CSV file to read
#
# @return dictionary of lists of each variable
#
def readCSVFile(inputfile):
  first_line_processed = False
  data = dict()
  variable_name_to_index = dict()

  # read data from input file into lists
  with open(inputfile) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      if (row):
        if (first_line_processed):
          for key in data:
            try:
              value = float(row[variable_name_to_index[key]])
            except:
              value = row[variable_name_to_index[key]]
            data[key].append(value)
        else:
          for i,entry in enumerate(row):
            variable_name_to_index[entry] = i
            data[entry] = list()
          first_line_processed = True

  # convert lists to numpy arrays
  for key in data:
    data[key] = np.array(data[key])

  return data


##
# Writes data to a CSV file
#
# @param[in] data       Dictionary of lists to output to file
# @param[in] filename   Name of the output file
# @param[in] append     Append data instead of over-writing it?
# @param[in] precision  Precision of entries in file
#
def writeCSVFile(data, filename, append=False, precision=5):
  output_file_exists = os.path.isfile(filename)

  if append:
    open_mode = 'a'

    # check that headers are the same
    if output_file_exists:
      existing_data = readCSVFile(filename)
      if set(data.keys()) != set(existing_data.keys()):
        raise Exception('The data to be appended does not have the same keys as the existing CSV.')
  else:
    open_mode = 'w'

  with open(filename, open_mode) as csvfile:
    writer = csv.writer(csvfile)

    keys = list(data.keys())

    # write header row if not appending
    if not append or not output_file_exists:
      writer.writerow(keys)

    # create number format string
    format_string = "%." + str(precision) + "e"

    # write data
    for i, item in enumerate(data[keys[0]]):
      row_data = list()
      for key in data:
        value = data[key][i]
        if isinstance(value, (int, float)):
          value_string = format_string % value
        else:
          value_string = value
        row_data.append(value_string)

      writer.writerow(row_data)



##
# Returns a list of file names that match a regular expression
#
# @param[in] regex_string   Regex string that file names should match
#
# @return list of file names that match the regular expression
#
def getFileNamesMatchingRegexString(regex_string):
  # get the subdirectory of the regex string
  subdirectory = os.path.dirname(regex_string)

  # remove the subdirectory from the regex
  regex_string = os.path.basename(regex_string)

  # get list of files in the subdirectory
  filelist = os.listdir(subdirectory)

  # create the regex
  regex = re.compile(regex_string)

  # loop through files in file list
  matched_file_list = list()
  for filename in filelist:
    if regex.search(filename):
      matched_file_list.append(filename)

  # add the subdirectory
  for i, item in enumerate(matched_file_list):
    matched_file_list[i] = subdirectory + '/' + matched_file_list[i]

  # return matches
  if len(matched_file_list) == 0:
    raise Exception('No match of files was found for the regex: ' + regex_string)
  else:
    return matched_file_list


##
# Returns a unique file name that matches a regular expression
#
# @param[in] regex_string   Regex string that file name should match
#
# @return unique file name that matches a regular expression
#
def getFileNameMatchingRegexString(regex_string):
  file_names = getFileNamesMatchingRegexString(regex_string)

  if len(file_names) > 1:
    raise Exception('Found multiple files matching regex: ' + regex_string)

  return file_names[0]


##
# Checks whether at least one file matches a regular expression string
#
# @param[in] regex_string   Regular expression string
#
# @return Does a file exist that matches the regular expression string?
#
def fileMatchingRegexStringExists(regex_string):
  # get the subdirectory of the regex string
  fields = regex_string.split('/')
  if (len(fields) > 1):
    subdirectory = '/'.join(fields[0:-1])
  else:
    subdirectory = '.'

  # remove the subdirectory from the regex
  regex_string = fields[-1]

  # get list of files in the subdirectory
  filelist = os.listdir(subdirectory)

  # create the regex
  regex = re.compile(regex_string)

  # loop through files in file list
  found_match = False
  for filename in filelist:
    if (regex.search(filename)):
      found_match = True

  return found_match


##
# Keeps the last file in a numbered series
#
# For a list of files of the format
#   somedir/filebase_####.someext
# keeps only the file with the largest #### and renames it.
#
# @param[in] regex      Regular expression for files in series
# @param[in] new_name   New name for last file in series
#
def keepFileWithMaxNumber(regex, new_name):
  # get list of files matching regex
  file_list = getFileNamesMatchingRegexString(regex)

  # get max file number
  max_file_number = 0
  i_max = 0
  for i, item in enumerate(file_list):
    file_number = int((item.split(".")[-2]).split("_")[-1])
    if file_number >= max_file_number:
      max_file_number = file_number
      i_max = i

  # copy latest file to new name
  os.system("cp " + file_list[i_max] + " " + new_name)

  # remove all of the matching files
  for item in file_list:
    os.system("rm " + item)
