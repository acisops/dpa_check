import os
import shutil
import tempfile

from ..dpa_check import dpa_check, model_path
from acis_thermal_check.regression_testing import run_answer_test, \
    run_image_test, run_model

def dpa_test_template(generate_answers, run_start, load_week, 
                      cmd_states_db='sybase'):
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)
    model_spec = os.path.join(model_path, "dpa_model_spec.json")
    out_dir = run_model("dpa", dpa_check, model_spec, run_start, 
                        load_week, cmd_states_db)
    run_answer_test("dpa", load_week, out_dir, generate_answers)
    run_image_test("1dpamzt", "dpa", load_week, out_dir, generate_answers)
    os.chdir(curdir)
    shutil.rmtree(tmpdir)

def test_dpa_may3016(generate_answers):
    run_start = "2016:122:12:00:00.000"
    load_week = "MAY3016"
    dpa_test_template(generate_answers, run_start, load_week)
