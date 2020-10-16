from ..dpa_check import model_path, DPACheck
from acis_thermal_check.regression_testing import \
    RegressionTester, all_loads
import pytest


@pytest.fixture(autouse=True, scope='module')
def dpa_rt(test_root):
    # ACIS state builder tests
    rt = RegressionTester(DPACheck, model_path, "dpa_test_spec.json",
                          test_root=test_root, sub_dir='sql')
    rt.run_models(state_builder='sql')
    return rt

# Prediction tests

@pytest.mark.parametrize('load', all_loads)
def test_prediction(dpa_rt, answer_store, load):
    if not answer_store:
        dpa_rt.run_test("prediction", load)
    else:
        pass

# Validation tests


@pytest.mark.parametrize('load', all_loads)
def test_validation(dpa_rt, answer_store, load):
    if not answer_store:
        dpa_rt.run_test("validation", load)
    else:
        pass
