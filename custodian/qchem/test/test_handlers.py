#!/usr/bin/env python

"""
Created on Dec 6, 2012
"""

from __future__ import division
import os
import shutil
from unittest import TestCase
import unittest
from custodian.qchem.handlers import QChemErrorHandler

__author__ = "Xiaohui Qu"
__version__ = "0.1"
__maintainer__ = "Xiaohui Qu"
__email__ = "xqu@lbl.gov"
__date__ = "Dec 6, 2013"


test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        "test_files", "qchem")
scr_dir = os.path.join(test_dir, "scr")


class QChemErrorHandlerTest(TestCase):
    def setUp(self):
        os.makedirs(scr_dir)
        os.chdir(scr_dir)

    def test_scf_rca(self):
        shutil.copyfile(os.path.join(test_dir, "hf_rca.inp"),
                        os.path.join(scr_dir, "hf_rca.inp"))
        shutil.copyfile(os.path.join(test_dir, "hf_rca.out"),
                        os.path.join(scr_dir, "hf_rca.out"))
        h = QChemErrorHandler(input_file="hf_rca.inp",
                              output_file="hf_rca.out")
        has_error = h.check()
        self.assertTrue(has_error)
        d = h.correct()
        self.assertEqual(d, {'errors': ['Bad SCF convergence',
                                        'Molecular charge is not found'],
                             'actions': ['rca_diis']})
        with open(os.path.join(test_dir, "hf_rca_tried_1.inp")) as f:
            ref = f.read()
        with open(os.path.join(scr_dir, "hf_rca.inp")) as f:
            ans = f.read()
        self.assertEqual(ref, ans)

        shutil.copyfile(os.path.join(test_dir, "hf_rca_tried_1.inp"),
                        os.path.join(scr_dir, "hf_rca_tried_1.inp"))
        shutil.copyfile(os.path.join(test_dir, "hf_rca.out"),
                        os.path.join(scr_dir, "hf_rca.out"))
        h = QChemErrorHandler(input_file="hf_rca_tried_1.inp",
                              output_file="hf_rca.out")
        has_error = h.check()
        self.assertTrue(has_error)
        d = h.correct()
        self.assertEqual(d, {'errors': ['Bad SCF convergence',
                                        'Molecular charge is not found'],
                             'actions': ['gwh']})
        with open(os.path.join(test_dir, "hf_rca_tried_2.inp")) as f:
            ref = f.read()
        with open(os.path.join(scr_dir, "hf_rca_tried_1.inp")) as f:
            ans = f.read()
        self.assertEqual(ref, ans)



    def tearDown(self):
        #shutil.rmtree(scr_dir)
        pass




if __name__ == "__main__":
    unittest.main()