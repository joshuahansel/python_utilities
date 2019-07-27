from termcolor import colored

def raiseException(msg):
  raise Exception(colored(msg, "red"))
