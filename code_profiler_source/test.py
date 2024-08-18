# This program takes delay time from its command line argument and sleeps for that time.

import sys
import time

def main():
    if len(sys.argv) != 3:
        print("Usage: python test.py <delay>")
        sys.exit(1)
    delay = float(sys.argv[1])
    loop_count = int(sys.argv[2])

    time.sleep(delay)

    for i in range(loop_count):
        print(f"Loop count: {i}")

    print("Slept for {} seconds".format(delay))
    print("Exiting...")

if __name__ == "__main__":
    main()