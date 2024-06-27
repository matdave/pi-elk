import argparse
from display.display import Display


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="display.py text on the OLED display.")
    parser.add_argument("line1", metavar="l1", type=str, help="text to display")
    parser.add_argument("line2", metavar="l2", type=str, help="text to display")
    parser.add_argument("line3", metavar="l3", type=str, help="text to display")
    parser.add_argument("line4", metavar="l4", type=str, help="text to display")

    args = parser.parse_args()

    display = Display()
    display.write(args.line1, args.line2, args.line3, args.line4)
