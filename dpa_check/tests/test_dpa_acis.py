from ..dpa_check import model_path, DPACheck
from acis_thermal_check.regression_testing import \
    RegressionTester, all_loads
import pytest

dpa_rt = RegressionTester(DPACheck, model_path)

# ACIS state builder tests

dpa_rt.run_models(state_builder='acis')

# Prediction tests


@pytest.mark.parametrize('load', all_loads)
def test_prediction(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

# Validation tests


@pytest.mark.parametrize('load', all_loads)
def test_validation(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)
