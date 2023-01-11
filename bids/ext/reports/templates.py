from pathlib import Path

import chevron
from rich import print


def render(template_name=None, data=None):

    template_file = Path(__file__).parent.joinpath("templates", "templates", template_name)

    with open(template_file) as template:

        print(data)

        args = {
            "template": template,
            "data": data,
            "partials_path": Path(__file__).parent.joinpath("templates", "partials"),
            #  keep is only available if chevron is installed from github
            # "keep": True,
        }
        tmp = chevron.render(**args)
        tmp = highlight_missing_tags(tmp)

        print()
        print(tmp)


def highlight_missing_tags(foo):
    foo = f"[blue]{foo}[/blue]"
    foo = foo.replace("{{", "[/blue][red]{{")
    foo = foo.replace("}}", "}}[/red][blue]")
    return foo


def footer():
    # Imported here to avoid a circular import
    from . import __version__

    return f"This section was (in part) generated automatically using pybids {__version__}."


def _mri_info(desc_data):
    return f"""repetition time, TR={desc_data["tr"]}ms;
    flip angle, FA={desc_data["flip_angle"]}<deg>;
field of view, FOV={desc_data["fov"]}mm;
matrix size={desc_data["matrix_size"]};
voxel size={desc_data["voxel_size"]}mm;"""


def anat_info(desc_data):
    return render(template_name="anat.mustache", data=desc_data)


def func_info(desc_data):

    render(template_name="func.mustache", data=desc_data)

    return f"""{desc_data["nb_runs"]} of {desc_data["task_name"]}
    {desc_data["variants"]}
{desc_data["seqs"]} {desc_data["multi_echo"]} fMRI data were collected
({_mri_info(desc_data)} echo time, TE={desc_data["echo_time"]}ms;
{desc_data["slice_order"]};
{desc_data["multiband_factor"]}; {desc_data["inplane_accel"]}).
Run duration was {desc_data["duration"]} minutes, during which
{desc_data["nb_vols"]} volumes were acquired."""


def dwi_info(desc_data):
    return f"""{desc_data["nb_runs"]} of {desc_data["variants"]}
{desc_data["seqs"]} diffusion-weighted (dMRI) data were collected ({_mri_info(desc_data)}
echo time, TE={desc_data["echo_time"]}ms;
b-values of {desc_data["bvals"]}acquired; {desc_data["dmri_dir"]} diffusion directions;
{desc_data["multiband_factor"]})."""


def fmap_info(desc_data):
    return f"""A {desc_data["variants"]} {desc_data["seqs"]} fieldmap ({_mri_info(desc_data)}
phase encoding: {desc_data["multiband_factor"]};
{desc_data["nb_slices"]} slices {desc_data["slice_order"]};
echo time 1 / 2, TE1/2={desc_data["te_1"]}/{desc_data["te_1"]};)
was acquired for the {desc_data["intended_for"]}.
"""
