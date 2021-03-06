import MeCab
import glob


def save_mecab_data(t, i):
    mecab = MeCab.Tagger()
    text = mecab.parse(t).split("\n")
    morph = ""
    for t in text:
        if t == "EOS":
            break
        t += ",O,O"
        morph += t + "\n"
    with open("data/{}.txt".format("tmp3"), mode="w") as f:  # 実際に使用する場合は下側のwithを使う
    # with open("data/exp/{}.txt".format(i), mode="w") as f:
        f.write(morph)

def make_exp_file():
    # files = glob.glob("data/raw/*")
    files = ["data/tmp1.txt"]  # 実際に使うときは上の一行を使う
    i = len(glob.glob("data/exp/*"))
    print(i)
    for file_name in files:
        with open(file_name, mode="r") as f:
            tmp = f.read()
        save_mecab_data(tmp, i)
        i += 1

if __name__ == "__main__":
    make_exp_file()