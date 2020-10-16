from ..dpa_check import DPACheck, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester
import os


def test_JUL3018A_viols(answer_store, test_root):
    answer_data = os.path.join(os.path.dirname(__file__), "answers",
                               "JUL3018A_viol.json")
    dpa_rt = RegressionTester(DPACheck, model_path, "dpa_test_spec.json",
                              test_root=test_root, sub_dir='viols')
    dpa_rt.check_violation_reporting("JUL3018A", answer_data,
                                     answer_store=answer_store)