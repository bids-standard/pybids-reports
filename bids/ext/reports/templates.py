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


def anat_info(desc_data):
    return render(template_name="anat.mustache", data=desc_data)


def func_info(desc_data):
    return render(template_name="func.mustache", data=desc_data)


def dwi_info(desc_data):
    return render(template_name="dwi.mustache", data=desc_data)


def fmap_info(desc_data):
    return render(template_name="fmap.mustache", data=desc_data)
