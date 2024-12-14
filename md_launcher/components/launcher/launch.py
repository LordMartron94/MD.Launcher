import sys

if __name__ == "__main__":
	args = sys.argv[1:]

	if len(args) < 1:
		print("A path to the configuration json file is required.")
		exit(1)
