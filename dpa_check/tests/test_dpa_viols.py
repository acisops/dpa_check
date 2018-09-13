from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester
import os

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)

def test_JUL3018A_viols():
    datestarts = ["2018:213:15:10:06.816", "2018:217:11:22:22.816"]
    datestops = ["2018:213:15:37:26.816", "2018:217:12:00:38.816"]
    temps = ["35.28", "35.48"]
    run_start = "2018:205:00:42:38.816"
    model_spec = os.path.join(os.path.dirname(__file__),
                              "JUL3018A_dpa.json")
    limits = {"yellow_hi": 37.2, "plan_limit_hi": 35.2}
    dpa_rt.check_violation_reporting("JUL3018A", model_spec, run_start,
                                     datestarts, datestops, temps,
                                     override_limits=limits)