#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from entregable4.e4_aux import entregable4


class TestEntregable4(unittest.TestCase):
    def __init__(self, test_name):
        super(TestEntregable4, self).__init__(test_name)
        self.mock1 = "entregable4/test/mock1.txt"
        self.mock2 = "entregable4/test/mock2.txt"

    def test_read_points(self):
        self.assertEquals(entregable4.read_points(self.mock1),
                          [(361.13310681656804, 424.1550499759833), (111.60536907441137, 368.2356070820062),
                           (424.0667744667676, 404.536653374835)])
        self.assertEquals(entregable4.read_points(self.mock2),
                          [(361.13310681656804, 424.1550499759833), (111.60536907441137, 368.2356070820062),
                           (424.0667744667676, 404.536653374835), (392.19218196852705, 352.979721943807)])

    def test_build_kd_tree(self):
        pass
