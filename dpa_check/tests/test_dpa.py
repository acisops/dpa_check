from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)

def test_dpa_loads(answer_store):
    dpa_rt.run_test_arrays(answer_store)

