#!/usr/bin/env python3
import argparse
import sys

MODULE_MAP = {
    "tmux": 0,
    "nvim": 0,
    "hyprland": 0,
}


def list_modules():
    """Simulate listing available modules."""
    pass


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
        output = f"Selected module: {args.module}"
        print(output)
        if args.out:
            try:
                with open(args.out, "w") as f:
                    f.write(output + "\n")
                print(f"Output written to {args.out}")
            except OSError as e:
                print(f"Error writing to {args.out}: {e}")
        else:
            print("(No output file specified; printed to stdout.)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
