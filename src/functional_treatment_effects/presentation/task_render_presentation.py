import subprocess

import pytask
from functional_treatment_effects.config import BLD
from functional_treatment_effects.config import PUBLIC
from functional_treatment_effects.config import SRC


SRC_FIGURES = SRC.joinpath("graphs")
BLD_FIGURES = BLD.joinpath("figures", "presentation")


src_figures = ["tim.jpeg", "compstat-repo-qr.png"]

bld_figures = ["data.png", "doubly_robust.png"]

src_figures = [SRC_FIGURES.joinpath(f) for f in src_figures]
bld_figures = [BLD_FIGURES.joinpath(f) for f in bld_figures]

dependencies = {f.name: f for f in src_figures + bld_figures}

for output_format in ["html", "pdf"]:

    kwargs = {
        "depends_on": {
            **dependencies,
            **{
                "source": SRC.joinpath("presentation", "main.md"),
                "scss": SRC.joinpath("presentation", "custom.scss").resolve(),
            },
        },
        "produces": PUBLIC.joinpath(f"slides.{output_format}"),
    }

    @pytask.mark.skip
    @pytask.mark.task(id=f"slides-{output_format}", kwargs=kwargs)
    def task_render_presentation(depends_on, produces):

        commands = [
            "marp",  # executable
            "--html",  # allows html code in markdown files
            "--allow-local-files",
            "--theme-set",
            str(depends_on["scss"]),  # use custom scss file
            "--output",
            str(produces),  # output file
        ]

        commands += ["--", depends_on["source"]]

        subprocess.call(commands)
