from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester
import os

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)

def test_JUL3018_viols():
    model_spec = os.path.join(os.path.dirname(__file__),
                              "JUL3018_dpa.json")
    dpa_rt.check_violation_reporting("JUL3018", model_spec)