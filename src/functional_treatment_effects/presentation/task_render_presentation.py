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
    compilation_steps=cs.marp(
        options=[
            "--html",  # allows html code in markdown files
            "--allow-local-files",
            f"--theme-set {str(SRC.joinpath('presentation', 'custom.scss'))}",
            # use custom scss file
        ]
    ),
)
@pytask.mark.depends_on(dependencies)
def task_render_presentation():
    pass
