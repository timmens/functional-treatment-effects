import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SRC


@pytask.mark.latex(
    script=SRC.joinpath("paper", "main.tex"),
    document=BLD.joinpath("paper", "main.pdf"),
)
def task_compile_paper():
    pass
