from pathlib import Path

DICT = {}


def main():
    path = Path("../work")
    anno_files = path.glob("*.anno")
    for anno_file in anno_files:
        with open(anno_file, encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            items = line.strip().split("\t")
            label = items[2]
            if label in DICT:
                DICT[label] += 1
            else:
                DICT[label] = 1


main()
data = []
for l, c in DICT.items():
    data.append((c, l))
data.sort()
for c, l in data:
    print(f"{c}\t{l}")
