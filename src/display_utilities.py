RESET  = '\033[0m'
BOLD   = '\033[1m'
BLACK  = '\033[30m'
WHITE  = '\033[37m'
RED    = '\033[31m'
GREEN  = '\033[32m'
CYAN   = '\033[36m'
YELLOW = '\033[33m'

##
# Prints text in color.
#
# @param[in] text    Text to color
# @param[in] color   Color to make text
#
# @returns Colored text
#
def colorText(text, color):
  colors = {"red": RED, "green": GREEN, "cyan": CYAN, "yellow": YELLOW, "white": WHITE}
  if color in colors:
    return colors[color] + text + RESET
  else:
    raise Exception("'%s' is not a valid color. Valid colors are: " % (color) + str(colors.keys()))
