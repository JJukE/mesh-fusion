import os
import argparse
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, help='Path to input directory.')
    args = parser.parse_args()

    paths = list(Path(args.data_dir).glob("**/*rendered.h5"))
    # paths_200k = []
    # paths_500k = []
    # for path in paths:
    #     if "500K" in str(path):
    #         paths_500k.append(path)
    #     elif "200K" in str(path):
    #         paths_200k.append(path)
    #     else:
    #         raise ValueError(path)
 
    # print("Number of paths containing 500K points: ", len(paths_200k))
    # print("Number of paths containing 200K points: ", len(paths_500k))
    print(paths)
    print(len(paths))

    for path in paths:
        # remove
        # if "model" in str(path):
        #     os.remove(str(path))
        
        # rename
        path.rename(path.with_name("{}_20".format(path.stem) + path.suffix)) # "**/*redered_20.h5"