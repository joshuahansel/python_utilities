import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import warnings

colors = [
    'k', 'indianred', 'orange', 'lightgreen', 'cornflowerblue', 'slateblue', 'orchid', 'turquoise',
    'peru'
]
linetypes = ['-', '--', ':']
markers = ["", ".", "x", "o", "s", "^", "D", "v", "*"]


class Plotter(object):

  def __init__(
      self,
      x_label,
      y_label,
      n_subplots=1,
      logscale_x=False,
      logscale_y=False,
      default_size_x=8,
      default_size_y=6):
    # get number of subplots in each dimension
    if isinstance(n_subplots, tuple):
      self.n_subplots_x, self.n_subplots_y = n_subplots
    else:
      self.n_subplots_y = n_subplots
      self.n_subplots_x = 1
    self.n_subplots = self.n_subplots_x * self.n_subplots_y
    self.current_subplot_index = 1

    # set figure size; default is 8 in X 6 in
    if self.n_subplots_x == 1:
      size_x = default_size_x
    elif self.n_subplots_x == 2:
      size_x = default_size_x * 2
    else:
      error("The number of sub-plots in x-direction must be <= 2")
    if self.n_subplots_y == 1:
      size_y = default_size_y
    elif self.n_subplots_y == 2:
      size_y = default_size_y * 2
    elif self.n_subplots_y == 3:
      size_y = default_size_y * 2
    else:
      error("The number of sub-plots in y-direction must be <= 3")
    plt.figure(figsize=(size_x, size_y))

    # use latex
    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    # get axes of first subplot
    self.ax = plt.subplot(self.n_subplots_y, self.n_subplots_x, 1)

    # turn off offset
    self.ax.get_yaxis().get_major_formatter().set_useOffset(False)

    # log scale
    self.logscale_x = logscale_x
    self.logscale_y = logscale_y

    # set the axis labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # flag for having set custom x range
    self.set_custom_x_range = False

    # legend
    self.legend_location = "upper right"
    self.put_legend_outside = False
    self.frame_legend = False
    self.legend_entries = list()

  def setLegendLocation(self, loc):
    self.legend_location = loc

  def adjustLeftMargin(self, margin):
    plt.subplots_adjust(left=margin)

  def useLegendFrame(self):
    self.frame_legend = True

  def setYFormat(self, y_format):
    self.ax.yaxis.set_major_formatter(FormatStrFormatter(y_format))

  def setXRange(self, xmin, xmax):
    self.set_custom_x_range = True
    self.xmin = xmin
    self.xmax = xmax
    self.ax.set_xlim([self.xmin, self.xmax])

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

  def putLegendOutside(self):
    self.put_legend_outside = True

    # shrink axis by 20% to allow room for legend outside of figure
    box = self.ax.get_position()
    self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

  def nextSubplot(self, x_label, y_label, logscale_x=False, logscale_y=False):
    # update logscale
    self.logscale_x = logscale_x
    self.logscale_y = logscale_y

    # create legend for previous subplot and then clear legend entries list
    if (self.put_legend_outside):
      self.ax.legend(
          self.legend_entries,
          loc='center left',
          frameon=self.frame_legend,
          bbox_to_anchor=(1, 0.5),
          prop={
              'size': 12
          })
    else:
      self.ax.legend(
          self.legend_entries,
          frameon=self.frame_legend,
          prop={'size': 12},
          loc=self.legend_location)
    self.legend_entries = list()

    # create new subplot
    self.current_subplot_index += 1
    self.ax = plt.subplot(self.n_subplots_y, self.n_subplots_x, self.current_subplot_index)

    # turn off offset
    self.ax.get_yaxis().get_major_formatter().set_useOffset(False)

    if self.put_legend_outside:
      box = self.ax.get_position()
      self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # set the x and y labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # set the x range if a custom x range was provided
    if (self.set_custom_x_range):
      self.ax.set_xlim([self.xmin, self.xmax])

  def addGrid(self):
    plt.grid(True)

  def addSet(self, x, y, set_name, color=-1, linetype=0, marker=0, scale=1):
    # scale y values
    y = [yi * scale for yi in y]

    if (self.logscale_x and self.logscale_y):
      plt.loglog(
          x,
          y,
          linetypes[linetype],
          color=colors[color],
          marker=markers[marker],
          markerfacecolor="none",
          markeredgecolor=colors[color])
    elif (self.logscale_x):
      plt.semilogx(
          x,
          y,
          linetypes[linetype],
          color=colors[color],
          marker=markers[marker],
          markerfacecolor="none",
          markeredgecolor=colors[color])
    elif (self.logscale_y):
      plt.semilogy(
          x,
          y,
          linetypes[linetype],
          color=colors[color],
          marker=markers[marker],
          markerfacecolor="none",
          markeredgecolor=colors[color])
    else:
      plt.plot(
          x,
          y,
          linetypes[linetype],
          color=colors[color],
          marker=markers[marker],
          markerfacecolor="none",
          markeredgecolor=colors[color])
    self.legend_entries.append(set_name)

  def save(self, outputfile):
    # create legend for final subplot
    if (self.put_legend_outside):
      self.ax.legend(
          self.legend_entries,
          loc='center left',
          frameon=self.frame_legend,
          bbox_to_anchor=(1, 0.5),
          prop={
              'size': 12
          })
    else:
      self.ax.legend(
          self.legend_entries,
          frameon=self.frame_legend,
          prop={'size': 12},
          loc=self.legend_location)

    # use tight layout to prevent clipping and overlap of axis labels
    # This issues a warning, so a context manager is used to catch it
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      plt.tight_layout()

    # save the figure
    plt.savefig(outputfile, dpi=300)
