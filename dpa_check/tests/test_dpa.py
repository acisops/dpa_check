from ..dpa_check import VALIDATION_LIMITS, \
    HIST_LIMIT, calc_model, model_path
from acis_thermal_check.regression_testing import \
    RegressionTester, test_loads
import pytest

dpa_rt = RegressionTester("1dpamzt", "dpa", model_path, VALIDATION_LIMITS,
                          HIST_LIMIT, calc_model)

for load in test_loads["normal"]:
    dpa_rt.run_model(load)

for load in test_loads["too"]+test_loads["stop"]:
    dpa_rt.run_model(load, interrupt=True)

image_list = dpa_rt.get_image_list()

# Prediction tests

@pytest.mark.parametrize('load', test_loads["normal"])
def test_normal_prediction(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

@pytest.mark.parametrize('load', test_loads["too"])
def test_too_prediction(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

@pytest.mark.parametrize('load', test_loads["stop"])
def test_stop_prediction(answer_store, load):
    dpa_rt.run_test("prediction", answer_store, load)

# Validation tests

@pytest.mark.parametrize('load', test_loads["normal"])
def test_normal_validation(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)

@pytest.mark.parametrize('load', test_loads["too"])
def test_too_validation(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)

@pytest.mark.parametrize('load', test_loads["stop"])
def test_stop_validation(answer_store, load):
    dpa_rt.run_test("validation", answer_store, load)

# Image tests

@pytest.mark.parametrize('load', test_loads["normal"])
@pytest.mark.parametrize('image', image_list)
def test_normal_images(answer_store, load, image):
    dpa_rt.run_test("image", answer_store, load, image=image)

@pytest.mark.parametrize('load', test_loads["too"])
@pytest.mark.parametrize('image', image_list)
def test_too_images(answer_store, load, image):
    dpa_rt.run_test("image", answer_store, load, image=image)

@pytest.mark.parametrize('load', test_loads["stop"])
@pytest.mark.parametrize('image', image_list)
def test_stop_images(answer_store, load, image):
    dpa_rt.run_test("image", answer_store, load, image=image)
