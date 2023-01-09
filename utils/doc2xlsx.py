import numpy as np
import pandas as pd
import names
import re
import time
import datetime
import random

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)
    

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

    reviewers = [names.get_full_name(gender='female') for _ in range (len(lines))]

    dates = [random_date("01/01/2021", "01/01/2022", random.random()) for _ in range(len(lines))]

    print(dates)

    reviews_df = pd.DataFrame(columns=["Reviews", "Ratings", "Authors", "Date"])
    reviews_df.Reviews = lines
    reviews_df.Ratings = ratings
    reviews_df.Authors = reviewers
    reviews_df.Date = dates

    print(reviews_df)

    return reviews_df
