import argparse
from pathlib import Path

from libvhls.project import Project
from libvhls.solution import Solution


# make a cli program that can do the following:
# - load a project and print its information
# - load a solution and print its information
# use argparse to make two subcommands, one for each of the above


def main_project(args: argparse.Namespace) -> None:
    print(f"Loading Vitis HLS project from: {args.project_dir}")
    try:
        project = Project.parse_from_disk(args.project_dir)
    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"Project name: {project.hls_app.name}")
    print(f"Project top: {project.hls_app.top}")
    print(f"Project type: {project.hls_app.project_type}")
    print("Project files:")
    for file in project.hls_app.files:
        print(f"  {file}")
    print("Project solutions:")
    for solution in project.hls_app.solutions:
        print(f"  {solution}")


def main_solution(args: argparse.Namespace) -> None:
    print(f"Loading Vitis HLS solution from: {args.solution_dir}")


if __name__ == "__main__":
    parser_main = argparse.ArgumentParser(
        description=(
            "A CLI program that uses libvhls to load and print information"
            " about a Vitis HLS projects and solutions"
        )
    )

    subparsers = parser_main.add_subparsers(
        title="subcommands",
        description="valid subcommands",
        help="additional help",
        required=True,
    )

    parser_project = subparsers.add_parser(
        "project",
        help="load a Vitis HLS project",
    )

    parser_project.add_argument(
        "project_dir",
        type=Path,
        help="The path to the Vitis HLS project",
    )

    parser_project.set_defaults(func=main_project)

    parser_solution = subparsers.add_parser(
        "solution",
        help="load a Vitis HLS solution",
    )

    parser_solution.add_argument(
        "solution_dir",
        type=Path,
        help="The path to the Vitis HLS solution",
    )

    parser_solution.set_defaults(func=main_solution)

    args = parser_main.parse_args()
    args.func(args)
