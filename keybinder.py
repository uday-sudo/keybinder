#!/usr/bin/env python3
import argparse
import sys
from parsers.tmux import TmuxParser

MODULE_MAP = {
    "tmux": TmuxParser,
    "nvim": 0,
    "hyprland": 0,
}


def list_modules():
    """Simulate listing available modules."""
    avaliable_modules = ""
    for key, value in MODULE_MAP.items():
        if value:
            avaliable_modules += f"{key}, "
    print(f"Avaliable modules: {avaliable_modules[:-2].strip()}")


def main():
    parser = argparse.ArgumentParser(
        description="Example CLI tool with --out, --module, and --list-modules options."
    )

    parser.add_argument(
        "--out",
        type=str,
        help="Path to the output file where results will be written.",
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write results to stdout.",
    )

    parser.add_argument(
        "--module",
        type=str,
        help="Specify the module name to use.",
    )

    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List all available modules and exit.",
    )

    args = parser.parse_args()

    # Handle --list-modules first (since it’s a standalone flag)
    if args.list_modules:
        list_modules()
        sys.exit(0)

    # Handle --module and --out
    if args.module:
        if MODULE_MAP.get(args.module):
            parser = MODULE_MAP[args.module]
            output = parser.convert_to_markdown()
        else:
            print(f"The module {args.module} is not implemented yet.")
            parser.print_help()
            sys.exit(0)
        if args.out:
            try:
                with open(args.out, "w") as f:
                    f.write(output + "\n")
                print(f"Output written to {args.out}")
            except OSError as e:
                print(f"Error writing to {args.out}: {e}")
        if args.stdout:
            print(output)
        if not args.stdout and not args.out:
            print("!!Output method not specified.")
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
