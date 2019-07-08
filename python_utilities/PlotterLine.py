import matplotlib.pyplot as plt

from PlotterBase import PlotterBase, colors, linetypes, markers
from file_utilities import readCSVFile

##
# Wrapper class to plot with Matplotlib
#
class PlotterLine(PlotterBase):
  def __init__(self, x_label, y_label, logscale_x=False, logscale_y=False, verbose=False):
    PlotterBase.__init__(self, x_label, y_label, logscale_x, logscale_y, verbose)

  def addSet(self, x, y, set_name, color=-1, linetype=1, marker=0, scale=1, n_points=50):
    # scale y values
    y = [yi * scale for yi in y]

    # determine the marker frequency
    if n_points > len(x):
      marker_frequency = 1
    else:
      marker_frequency = int(round(len(x) / n_points))

    color_index = color % len(colors)
    marker_index = marker % len(markers)
    linetype_index = linetype % len(linetypes)

    if (self.logscale_x and self.logscale_y):
      plt.loglog(x,y,linetypes[linetype_index],color=colors[color_index],
        marker=markers[marker_index],markerfacecolor="none",markeredgecolor=colors[color_index],markevery=marker_frequency)
    elif (self.logscale_x):
      plt.semilogx(x,y,linetypes[linetype_index],color=colors[color_index],
        marker=markers[marker_index],markerfacecolor="none",markeredgecolor=colors[color_index],markevery=marker_frequency)
    elif (self.logscale_y):
      plt.semilogy(x,y,linetypes[linetype_index],color=colors[color_index],
        marker=markers[marker_index],markerfacecolor="none",markeredgecolor=colors[color_index],markevery=marker_frequency)
    else:
      plt.plot(x,y,linetypes[linetype_index],color=colors[color_index],
        marker=markers[marker_index],markerfacecolor="none",markeredgecolor=colors[color_index],markevery=marker_frequency)
    self.legend_entries.append(set_name)

##
# Makes line plots given a number of lists.
#
def makeLinePlots(base_name, y_labels, scaling_factors, y_bounds_list,
    legend_locations, var_name_lists, set_label_lists, block_names):

  n_blocks = len(block_names)

  # load data
  data = list()
  for i, block_name in enumerate(block_names):
    data.append(dict())
    for var_name_list in var_name_lists:
      for var_name in var_name_list:
        file_name = base_name + "_" + var_name + "_" + block_name + ".csv"
        block_data = readCSVFile(file_name)
        data[i]["x"] = block_data["x"]
        data[i][var_name] = block_data[var_name]

  # make plots
  def makeLinePlot(y_label, var_name_list, set_label_list, scaling, y_bounds, leg_loc):
    plotter = Plotter("$x$", y_label)
    for i in xrange(n_blocks):
      x = data[i]["x"]
      for j, var_name in enumerate(var_name_list):
        plotter.addSet(x, data[i][var_name], set_label_list[j] + ", Mesh " + str(i + 1),
          color=i + 1, linetype=j, marker=i + 1, scale=scaling)
    if y_bounds:
      plotter.setYRange(y_bounds[0], y_bounds[1])
    plotter.setLegendLocation(leg_loc)
    plotter.save(base_name + "_" + var_name_list[0] + ".pdf")

  for y_label, var_name_list, set_label_list, scaling, y_bounds, leg_loc in \
      zip(y_labels, var_name_lists, set_label_lists, scaling_factors, y_bounds_list, legend_locations):
    makeLinePlot(y_label, var_name_list, set_label_list, scaling, y_bounds, leg_loc)
