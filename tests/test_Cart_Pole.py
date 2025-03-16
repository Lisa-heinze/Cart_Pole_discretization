import argparse
from unittest import TestCase
import numpy as np

from Cart_Pole import make_space


class Test(TestCase):

    def test_linspace_default(self):
        args = argparse.Namespace(geom=False, cut_not_zero=False, cut_close_zero=False)
        result = make_space(10, 5, args)
        expected = np.array([-10., -7.5, -5., -2.5, 0, 2.5, 5., 7.5, 10.])
        assert np.allclose(result, expected)

    def test_geomspace_default(self):
        args = argparse.Namespace(geom=True, cut_not_zero=False, cut_close_zero=False)
        result = make_space(10, 5, args)
        expected = np.array([-10, -5.04010535, -2.31662479, -0.82116029, -0., 0.82116029, 2.31662479, 5.04010535, 10])
        assert np.allclose(result, expected)

    def test_linspace_cut_not_zero(self):
        args = argparse.Namespace(geom=False, cut_not_zero=True, cut_close_zero=False)
        result = make_space(10, 5, args)
        expected = np.array([-10., -8.75, -6.25, -3.75, -1.25, 1.25, 3.75, 6.25, 8.75, 10.])
        assert np.allclose(result, expected)

    def test_geomspace_cut_not_zero(self):
        args = argparse.Namespace(geom=True, cut_not_zero=True, cut_close_zero=False)
        result = make_space(10, 5, args)
        expected = np.array(
            [-10., -9.58941986, -4.62952521, -1.90604465, -0.41058014, 0.41058014, 1.90604465, 4.62952521, 9.58941986,
             10.])
        assert np.allclose(result, expected)

    def test_linspace_cut_near_zero(self):
        args = argparse.Namespace(geom=False, cut_not_zero=False, cut_close_zero=True)
        result = make_space(10, 5, args)
        assert not 0 in result
        assert -10 >= result[0]
        assert 10 <= result[-1]

    def test_geomspace_cut_near_zero(self):
        args = argparse.Namespace(geom=True, cut_not_zero=False, cut_close_zero=True)
        result = make_space(10, 5, args)
        assert not 0 in result
        assert -10 >= result[0]
        assert 10 <= result[-1]

    def test_single_element(self):
        args = argparse.Namespace(geom=False, cut_not_zero=False, cut_close_zero=False)
        result = make_space(10, 1, args)
        expected = np.array([0])
        assert np.allclose(result, expected)
