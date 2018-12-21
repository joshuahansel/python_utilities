import matplotlib.pyplot as plt
import numpy as np

from PlotterBase import PlotterBase, colors, linetypes, markers

##
# Class for creating bar plots with Matplotlib.
#
class PlotterBar(PlotterBase):
  def __init__(self, x_label, y_label, logscale_x=False, logscale_y=False, verbose=False):
    PlotterBase.__init__(self, x_label, y_label, logscale_x, logscale_y, verbose)

  ##
  # Makes a bar plot.
  #
  # @param[in] x_sub_labels   [x_sub_label], where "x_sub_label" is a x-axis sub-label.
  # @param[in] set_labels     [set_label], where "set_label" is a plot set label.
  # @param[in] y_values       {x_sub_label: {set_label : y}}, where "y" is a y-value.
  # @param[in] y_stddev       {x_sub_label: {set_label : stddev}}, where "stddev" is a standard deviation value.
  #
  def makeBarPlot(self, x_sub_labels, set_labels, y_values, y_stddev=None):
    # get sizes
    n_sets = len(set_labels)
    n_x_subs = len(x_sub_labels)

    # width of bars; 1.0 would leave no space between bars
    bar_width = 1.0 / (n_sets + 2.0)

    # color of error bar; 0.0 is black, 1.0 is white
    error_config = {'ecolor': '0.3'}

    # add each bar; loop over sets
    indices = np.arange(n_x_subs)
    for i_set, set_label in enumerate(set_labels):
      set_label = set_labels[i_set]

      bar_positions = [i + bar_width * i_set for i in indices]

      values = list()
      for x_sub_label in x_sub_labels:
        values.append(y_values[x_sub_label][set_label])

      if y_stddev:
        stddevs = list()
        for x_sub_label in x_sub_labels:
          stddevs.append(y_stddev[x_sub_label][set_label])

        self.ax.bar(bar_positions, values, bar_width,
                    color=colors[i_set + 1], yerr=stddevs, error_kw=error_config)
      else:
        self.ax.bar(bar_positions, values, bar_width, color=colors[i_set + 1])

      self.legend_entries.append(set_labels[i_set])

    # add x sub-labels
    plt.xticks([r + 0.5 * bar_width * (n_sets - 1) for r in range(len(x_sub_labels))], x_sub_labels)
    plt.tick_params(axis='x', which='both', bottom=False)
