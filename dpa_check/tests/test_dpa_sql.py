from ..dpa_check import model_path, DPACheck
from acis_thermal_check.regression_testing import \
    RegressionTester, all_loads
import pytest

dpa_rt = RegressionTester(DPACheck, model_path, "dpa_test_spec.json")

# SQL state builder tests

dpa_rt.run_models(state_builder='sql')

# Prediction tests


@pytest.mark.parametrize('load', all_loads)
def test_prediction(answer_store, load):
    if not answer_store:
        dpa_rt.run_test("prediction", load)
    else:
        pass

# Validation tests


@pytest.mark.parametrize('load', all_loads)
def test_validation(answer_store, load):
    if not answer_store:
        dpa_rt.run_test("validation", load)
    else:
        pass
