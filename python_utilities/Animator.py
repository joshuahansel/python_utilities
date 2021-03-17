import matplotlib.pyplot as plt
from Player import Player

x_width_per_column = 8
y_width_per_row = 6

class Animator(object):
  def __init__(self, n_subplots_x=1, n_subplots_y=1):
    self.n_subplots_x = n_subplots_x
    self.n_subplots_y = n_subplots_y

    self.i_subplot = -1
    self.ax_list = list()
    self.ax_lines = list()
    self.x = list()
    self.y = list()
    self.legend_entries = list()

    self.fig = plt.figure(figsize=(x_width_per_column * n_subplots_x, y_width_per_row * n_subplots_y))

  def nextSubplot(self, x_label, y_label, x_lim=None, y_lim=None, pad=False, logscale_y=False):
    self.i_subplot += 1

    # add legend for previous subplot, if there is one
    if self.i_subplot != 0:
      self.finishSubplot(self.i_subplot-1)

    self.ax_list.append(plt.subplot(self.n_subplots_y, self.n_subplots_x, self.i_subplot+1))

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if x_lim:
      x_min, x_max = x_lim
      self.ax_list[self.i_subplot].set_xlim([x_min, x_max])
      self.autoscale_x = False
    else:
      self.autoscale_x = True

    if y_lim:
      y_min, y_max = y_lim
      self.ax_list[self.i_subplot].set_ylim([y_min, y_max])
      self.autoscale_y = False
    else:
      self.autoscale_y = True

    if logscale_y:
      self.ax_list[self.i_subplot].set_yscale('log')

    self.pad = pad

    self.legend_entries = list()
    self.x.append(list())
    self.y.append(list())
    self.ax_lines.append(list())

  def finishSubplot(self, i_subplot):
    self.ax_list[i_subplot].legend(self.legend_entries, frameon=False)

    if self.autoscale_x:
      x_min = min([self.minOverTimesteps(xj) for xj in self.x[i_subplot]])
      x_max = max([self.maxOverTimesteps(xj) for xj in self.x[i_subplot]])
      self.ax_list[i_subplot].set_xlim([x_min, x_max])

    if self.autoscale_y:
      y_min = min([self.minOverTimesteps(yj) for yj in self.y[i_subplot]])
      y_max = max([self.maxOverTimesteps(yj) for yj in self.y[i_subplot]])
      if self.pad:
        pad = 0.05 * abs(y_max)
        y_min -= pad
        y_max += pad
      self.ax_list[i_subplot].set_ylim([y_min, y_max])

  def addSet(self, x, y, label):
    self.x[self.i_subplot].append(x)
    self.y[self.i_subplot].append(y)
    self.legend_entries.append(label)

    line, = plt.plot([], [])
    self.ax_lines[self.i_subplot].append(line)

  def playerUpdate(self, frame):
    lines = ()
    for i_subplot, ax in enumerate(self.ax_list):
      for j_line, line in enumerate(self.ax_lines[i_subplot]):
        line.set_data(self.x[i_subplot][j_line][frame], self.y[i_subplot][j_line][frame])
        lines = lines + (line,)
    return lines

  def show(self):
    self.finishSubplot(self.i_subplot)

    n_steps = len(self.x[0][0])
    timesteps = range(n_steps)

    ani = Player(self.fig, self.playerUpdate, frames=timesteps, maxi=n_steps-1)
    plt.show()

  def minOverTimesteps(self, x):
    x_min = [min(xi) for xi in x]
    return min(x_min)

  def maxOverTimesteps(self, x):
    x_max = [max(xi) for xi in x]
    return max(x_max)
