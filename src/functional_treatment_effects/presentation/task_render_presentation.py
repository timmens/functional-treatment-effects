import pytask
import pytask_markdown.compilation_steps as cs
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import SRC


SRC_FIGURES = SRC.joinpath("graphs")
BLD_FIGURES = BLD.joinpath("figures", "presentation")


src_figures = []
bld_figures = ["data.png", "doubly_robust.png"]

src_figures = [SRC_FIGURES.joinpath(f) for f in src_figures]
bld_figures = [BLD_FIGURES.joinpath(f) for f in bld_figures]

dependencies = {f.name: f for f in src_figures + bld_figures}


@pytask.mark.markdown(
    script=SRC.joinpath("presentation", "main.md"),
    document=BLD.joinpath("presentation", "main.pdf"),
    css=SRC.joinpath("presentation", "custom.scss"),
    compilation_steps=cs.marp(options=["--html", "--allow-local-files"]),
)
@pytask.mark.depends_on(dependencies)
def task_render_presentation():
    pass
