import textwrap

import yaml

import gradcafe

UNIV_LIST = yaml.load(open("univ.yaml"), yaml.Loader)


def run(university_list, season=""):
    for univ in university_list["univ"]:
        institution = univ["inst"]
        degree = univ["degree"]
        program = univ["program"] if "program" in univ else "Computer Science"

        print(f"Institution: {institution}")
        for result in gradcafe.get_results(
            gradcafe.make_params(
                institution=institution, degree=degree, program=program, season=season
            ),
            pages=1,
        ):
            print(
                "\t",
                result["added_date"],
                result["decision"],
                result["department"],
                result["received_date"],
            )
            print(
                "\n\t\t".join(
                    textwrap.wrap(
                        result["description"], width=60, initial_indent="\n\t\t >> "
                    )
                )
            )

            print("\n\t\t", " ".join(result["raw_stats"]))


if __name__ == "__main__":
    run(UNIV_LIST, UNIV_LIST["config"]["season"])
