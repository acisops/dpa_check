from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    run_test_arrays

def test_dpa_loads(answer_store):
    run_test_arrays("1dpamzt", "dpa", model_path,
                    [VALIDATION_LIMITS, HIST_LIMIT, calc_model],
                    answer_store)

