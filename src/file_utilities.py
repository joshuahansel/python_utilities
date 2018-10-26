import os
import numpy as np
import re
import csv


## Reads data from a CSV file
# @param inputfile  name of the file to read
# @return dictionary of lists of each variable
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
            data[key].append(float(row[variable_name_to_index[key]]))
        else:
          for i, entry in enumerate(row):
            variable_name_to_index[entry] = i
            data[entry] = list()
          first_line_processed = True

  # convert lists to numpy arrays
  for key in data:
    data[key] = np.array(data[key])

  return data


# data should be a dictionary of lists of the data points
def writeCSVFile(data, output_file):
  with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile)

    # write header row
    key_list = [key for key in data]
    print(key_list)
    writer.writerow(key_list)

    # write data
    for i, item in enumerate(data[key_list[0]]):
      row_data = [data[key][i] for key in data]
      writer.writerow(row_data)


def getFileNamesMatchingRegexString(regex_string):
  # get the subdirectory of the regex string
  fields = regex_string.split('/')
  if len(fields) > 1:
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


# For a list of files of the format
#   somedir/filebase_####.someext
# keeps only the file with the largest #### and renames it.
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
