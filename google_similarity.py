import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import math, sys, time, random, collections
import numpy as np
import pandas as pd

from urllib.request import urlopen


def PMID(d_w1, d_w2, d_w1_w2, D):
    """
    :param d_w1: no of documents containing word w1
    :param d_w2: no of documents containing word w1
    :param d_w1_w2: no of documents containing both word w1 and word w2
    :param D: size of corpus, in this case number of pages including "the"
    :return: document-based pointwise mutual information
    """

    if d_w1 <= 0 or d_w2 <= 0 or d_w1_w2 <= 0:
        return -10000

    return math.log(d_w1_w2, 2) - math.log(float(d_w1*d_w2/D), 2)


def NGD(f_w1, f_w2, f_w1_w2, N):
    """
    :param f_w1: no of documents containing word w1
    :param f_w2: no of documents containing word w1
    :param f_w1_w2: no of documents containing both word w1 and word w2
    :param N: size of corpus, in this case number of pages including "the"
    Returns:
     NGD (float)
    """
    N = math.log(N, 2)
    if f_w1 <= 0 or f_w2 <= 0 or f_w1_w2 <= 0:
        return -10000

    f_w1 = math.log(f_w1, 2)
    f_w2 = math.log(f_w2, 2)
    f_w1_w2 = math.log(f_w1_w2, 2)
    return (max(f_w1, f_w2) - f_w1_w2) / (N - min(f_w1, f_w2))

def number_of_results(text):
    """Returns the number of Google results for a given query."""
    # headers = {'User-Agent': UserAgent().firefox}
    # sleep(5, 10)
    # print(headers)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    URL = "https://www.google.com/search?q={}".format(text.replace(" ","+"))
    result = requests.get(URL, headers=headers)

    soup = BeautifulSoup(result.content, 'html.parser')

    total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True,
                                                                       recursive=False)
    if total_results_text:
        results_num = ''.join([num for num in total_results_text if
                               num.isdigit()])
        return int(results_num)

    return 0


def test_NGD(comp1, comp2):
    f_comp1 = number_of_results(comp1)
    f_comp2 = number_of_results(comp2)
    f_comp1_comp2 = number_of_results(f"{comp1} {comp2}")

    N = 25270000000000

    return NGD(f_comp1, f_comp2, f_comp1_comp2, N)


if __name__ == "__main__":
    print(test_NGD("samsung", "apple"))
