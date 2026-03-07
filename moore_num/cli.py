import argparse
import sys
from .converter import convert_to_text, text_to_num

def main():
    parser = argparse.ArgumentParser(description="Convert numbers to Mooré text and vice versa.")
    parser.add_argument("input", help="The number (integer) or Mooré text to convert.")
    parser.add_argument("--money", action="store_true", help="Enable money scaling (factor of 5).")
    parser.add_argument("--reverse", "-r", action="store_true", help="Convert text to number.")
    
    args = parser.parse_args()
    
    try:
        if args.reverse:
            print(text_to_num(args.input, is_money=args.money))
        else:
            try:
                num = int(args.input)
                print(convert_to_text(num, is_money=args.money))
            except ValueError:
                print("Error: Input must be an integer for forward conversion. Use --reverse for text-to-number.", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
