import functional_treatment_effects.config as config
import pytask
import pytest


@pytest.mark.end_to_end
def test_pytask_call(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "BLD", tmp_path.joinpath("bld").resolve())
    session = pytask.main({"paths": config.ROOT})
    assert session.exit_code == pytask.ExitCode.OK
