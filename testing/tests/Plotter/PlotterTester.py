import unittest
import filecmp

from PlotterLine import PlotterLine
from PlotterBar import PlotterBar


class PlotterTester(unittest.TestCase):

  def setUp(self):
    pass

  def testLinePlot(self):
    plotter = PlotterLine('x', 'y')
    x = [1, 2, 3]
    y1 = [1, 2, 3]
    y2 = [2, 4, 6]
    plotter.addSet(x, y1, 'y1', color=1)
    plotter.addSet(x, y2, 'y2', color=2)

    path = "testing/tests/Plotter/"
    output_file = path + "test_line_plot.jpg"
    gold_file = path + "gold/test_line_plot.jpg"

    plotter.save(output_file)

    self.assertTrue(filecmp.cmp(output_file, gold_file))

  def testBarPlot(self):
    plotter = PlotterBar('x', 'y')
    x_sub_labels = ["Group1", "Group2"]
    set_values = ["Set1", "Set2", "Set3"]
    y_values = {"Group1" : {"Set1" : 1.0, "Set2" : 2.0, "Set3" : 3.0},
                "Group2" : {"Set1" : 1.5, "Set2" : 2.5, "Set3" : 3.5}}
    y_stddev = {"Group1" : {"Set1" : 0.1, "Set2" : 0.2, "Set3" : 0.3},
                "Group2" : {"Set1" : 0.2, "Set2" : 0.3, "Set3" : 0.4}}
    plotter.makeBarPlot(x_sub_labels, set_values, y_values, y_stddev)

    path = "testing/tests/Plotter/"
    output_file = path + "test_bar_plot.jpg"
    gold_file = path + "gold/test_bar_plot.jpg"

    plotter.save(output_file)

    self.assertTrue(filecmp.cmp(output_file, gold_file))
