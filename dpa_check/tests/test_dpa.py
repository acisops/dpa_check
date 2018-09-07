from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester, all_loads
import pytest

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)

# ACIS state builder tests

dpa_rt.run_models(state_builder='acis')

# Prediction tests

@pytest.mark.parametrize('load', all_loads)
def test_prediction_acis(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

# Validation tests

@pytest.mark.parametrize('load', all_loads)
def test_validation_acis(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)

# SQL state builder tests

dpa_rt.run_models(state_builder='sql')

# Prediction tests

@pytest.mark.parametrize('load', all_loads)
def test_prediction_sql(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

# Validation tests

@pytest.mark.parametrize('load', all_loads)
def test_validation_sql(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)

