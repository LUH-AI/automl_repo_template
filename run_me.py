from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--id")
args = parser.parse_args()
print(f"Hello, I am a test! My ID is {args.id}")