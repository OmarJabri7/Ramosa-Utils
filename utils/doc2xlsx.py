import numpy as np
import pandas as pd
import names
import re


def gen_reviews(data):
    all_lines = ''.join(data).replace("\n", "").split("- Ramosa Ltd")
    all_lines = [x for x in all_lines if x != ""]
    lines = list()
    for line in all_lines:
        if re.search('[a-zA-Z]', line): lines.append(line)
    print(f"Number of reviews: {len(lines)}")
    lines = [line.strip().replace("-\r\r", "") for line in lines]
    lines = [line.strip().replace("\r\r", "") for line in lines]
    lines = [line.strip().replace("--", "") for line in lines]
    lines = [line.strip().replace("try: pass", "") for line in lines]
    ratings = np.random.uniform(low=4.5, high=5, size=(len(lines),)).round(1)

    reviewers = [names.get_full_name() for _ in range (len(lines))]

    reviews_df = pd.DataFrame(columns=["Reviews", "Ratings", "Authors"])
    reviews_df.Reviews = lines
    reviews_df.Ratings = ratings
    reviews_df.Authors = reviewers

    return reviews_df


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-d', '--doc', help='doc file', type=str)
#
#     args = parser.parse_args()
#
#     doc_file = args.doc
#
#     with open(doc_file, "r",) as file_in:
#         lines = []
#         for line in file_in:
#             if re.search('[a-zA-Z]', line): lines.append(line)
#     lines_arr = ''.join(lines).replace("\n", "").split("- Ramosa Ltd")
#     lines_arr = [x for x in lines_arr if x != ""]
#     print(f"Number of reviews: {len(lines_arr)}")
#
#     ratings = np.random.uniform(low=4.5, high=5, size=(len(lines_arr),)).round(1)
#
#     names = [names.get_full_name() for _ in range (len(lines_arr))]
#
#     reviews_df = pd.DataFrame(columns=["Reviews", "Ratings", "Authors"])
#     reviews_df.Reviews = lines_arr
#     reviews_df.Ratings = ratings
#     reviews_df.Authors = names
#
#     reviews_df.to_csv("Reviews.csv", index= False)
#
