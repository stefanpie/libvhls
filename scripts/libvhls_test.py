import argparse


def main(args):
    if args.say_hello:
        print("Hello, world!")
    if args.say_goodbye:
        print("Goodbye, world!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A test cli program for libvhls")

    parser.add_argument(
        "--say-hello",
        action="store_true",
        help="Say hello to the world",
    )

    parser.add_argument(
        "--say-goodbye",
        action="store_true",
        help="Say goodbye to the world",
    )

    args = parser.parse_args()
    print(args)
    if not args.say_hello and not args.say_goodbye:
        parser.print_help()
    else:
        main(args)
