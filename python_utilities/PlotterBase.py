import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import warnings

colors = ['k','indianred','orange','lightgreen','cornflowerblue','slateblue','orchid','turquoise','peru']
linetypes = [' ','-','--',':']
markers = ["", ".", "x", "o", "s", "^", "D", "v", "*"]

##
# Base class wrapper for Matplotlib
#
class PlotterBase(object):
  def __init__(self, x_label, y_label, logscale_x=False, logscale_y=False, verbose=False):

    plt.figure(figsize=(8, 6))
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    # get axes
    self.ax = plt.subplot(1, 1, 1)

    # turn off offset
    self.ax.get_yaxis().get_major_formatter().set_useOffset(False)

    # log scale
    self.logscale_x = logscale_x
    self.logscale_y = logscale_y

    # axis labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # legend
    self.legend_location = "upper right"
    self.frame_legend = False
    self.legend_entries = list()

    # verbosity
    self.verbose = verbose

  def setLegendLocation(self, loc):
    self.legend_location = loc

  def useLegendFrame(self):
    self.frame_legend = True

  def setYFormat(self, y_format):
    self.ax.yaxis.set_major_formatter(FormatStrFormatter(y_format))

  def setXRange(self, xmin, xmax):
    self.ax.set_xlim([xmin, ymin])

  def setYRange(self, ymin, ymax):
    self.ax.set_ylim([ymin, ymax])

  def fixNearConstantPlot(self, dy_rel_min=1e-8):
    ymin, ymax = self.ax.get_ylim()
    dy = ymax - ymin
    max_abs_y = max(abs(ymin), abs(ymax))
    dy_rel = dy / max_abs_y
    if (dy_rel < dy_rel_min):
      yavg = 0.5 * (ymin + ymax)
      dy_new = dy_rel_min * max_abs_y
      ymin_new = yavg - 0.5 * dy_new
      ymax_new = yavg + 0.5 * dy_new
      self.setYRange(ymin_new, ymax_new)

  ##
  # Saves the plot to a file.
  #
  # @param[in] outputfile   Name of the output file.
  #
  def save(self, outputfile):
    # legend
    self.ax.legend(self.legend_entries, frameon=self.frame_legend, prop={'size':12}, loc=self.legend_location)

    # use tight layout to prevent clipping and overlap of axis labels
    # This issues a warning, so a context manager is used to catch it
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      plt.tight_layout()

    # save the figure
    plt.savefig(outputfile, dpi=300)

    if self.verbose:
      print("Created plot '%s'." % (outputfile))
