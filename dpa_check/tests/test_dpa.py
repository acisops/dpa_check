from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester, test_loads
import pytest

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)


@pytest.mark.parametrize('load', test_loads["normal"])
def test_normal_results(answer_store, load):
    dpa_rt.run_answer_test(answer_store, load)


@pytest.mark.parametrize('load', test_loads["normal"])
def test_normal_images(answer_store, load):
    dpa_rt.run_image_test(answer_store, load)


@pytest.mark.parametrize('load', test_loads["too"])
def test_too_results(answer_store, load):
    dpa_rt.run_answer_test(answer_store, load)


@pytest.mark.parametrize('load', test_loads["too"])
def test_too_images(answer_store, load):
    dpa_rt.run_image_test(answer_store, load)


@pytest.mark.parametrize('load', test_loads["stop"])
def test_stop_results(answer_store, load):
    dpa_rt.run_answer_test(answer_store, load)


@pytest.mark.parametrize('load', test_loads["stop"])
def test_stop_images(answer_store, load):
    dpa_rt.run_image_test(answer_store, load)
