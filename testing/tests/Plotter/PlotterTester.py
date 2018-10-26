import unittest
import filecmp

from Plotter import Plotter


class PlotterTester(unittest.TestCase):

  def setUp(self):
    pass

  def testPlot(self):
    plotter = Plotter('x', 'y', 2)
    x = [1, 2, 3]
    y1 = [1, 2, 3]
    y2 = [2, 4, 6]
    z1 = [2, 3, 5]
    z2 = [0, 1, 4]
    plotter.addSet(x, y1, 'y1', color=1)
    plotter.addSet(x, y2, 'y2', color=2)
    plotter.nextSubplot('x', 'z')
    plotter.addSet(x, z1, 'z1', color=3)
    plotter.addSet(x, z2, 'z2')

    path = "testing/tests/Plotter/"
    output_file = path + "test_plot.jpg"
    gold_file = path + "gold/test_plot.jpg"

    plotter.save(output_file)

    self.assertTrue(filecmp.cmp(output_file, gold_file))
