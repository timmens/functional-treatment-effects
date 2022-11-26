import subprocess

from functional_treatment_effects.config import ROOT


def test_pytask():
    subprocess.call("pytask", cwd=ROOT)
