from google_search import GoogleSearchClient


import time
import pickle
import pandas as pd
from typing import List, Dict, Tuple, Any


import logging

logging.basicConfig(filename="calculating_company_frequencies_example.txt",
                        filemode='a',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

logging.info("Frequency of competitors in Web")


def get_company_frequencies(search_client: GoogleSearchClient, company_id_name_tuples: List[Tuple[str, str]]) -> Dict[str, Any]:
    """
    :param search_client: GoogleSearchClient object
    :param company_id_name_tuples: list of [company_name, id] tuples, e.g.: [["Apple", "idejbxspa"],["Samsung", "iddjssjks"],...]
    :return: dictionary of frequency, keys are id, values are name and frequency,
    e.g.: {"idejbxspa": ["Apple", 182637181], "iddjssjks": ["Samsung", 3829172]}
    """
    frequencies = dict()
    for name, id_ in company_id_name_tuples:
        try:
            no_ = search_client.search_count(f'"{name}"')
        except Exception as e:
            logging.error(e)
            continue
        frequencies[id_] = [name, no_]
        time.sleep(0.7)

    return frequencies


def get_competitor_frequencies(search_client: GoogleSearchClient, competitor_id_names_tuples: List[Any]) -> Dict[Any, Any]:
    """
        :param search_client: GoogleSearchClient object
        :paramcompetitor_id_names_tuple: list of names and ids of pair companies [company_name1, id1, company_name2, id2],
         e.g.: [[["Apple", "idejbxspa"],["Samsung", "iddjssjks"]],...]
        :return: dictionary of co-occurrence frequency, keys are combined ids, values number of pages companies occurred together,
        e.g.: {("idejbxspa", "iddjssjks"): 36171, ...}
        """
    frequencies = dict()
    for c1_name, id1, c2_name, id2 in competitor_id_names_tuples:
        try:
            no_ = search_client.search_count(f'"{c1_name}" "{c2_name}"')
        except Exception as e:
            logging.error(e)
            continue
        frequencies[(id1, id2)] = no_
        time.sleep(0.7)

    return frequencies

from argparse import ArgumentParser

if __name__ == '__main__':

    gclient = GoogleSearchClient()
    parser = ArgumentParser()
    parser.add_argument("-path_to_company_names", "--company_names_path")
    parser.add_argument("-path_to_company_pairs", "--pair_names_path")

    args = parser.parse_args()

    df_companies = pd.read_csv(args.company_names_path)
    company_ids = df_companies["Column_1"].tolist()
    company_names = df_companies["Column_2"].tolist()

    df_competitors = pd.read_csv(args.pair_names_path)
    pair_company_ids1 = df_competitors["ID1"].tolist()
    pair_company_ids2 = df_competitors["ID2"].tolist()

    logging.info("Getting Individual Company Frequencies from Google")

    company_name_tuples = list(zip(company_names, company_ids))
    company_frequencies = get_company_frequencies(gclient, company_name_tuples)

    with open(f"company_frequencies_google_api_example.pickle", "wb") as f:
        pickle.dump(company_frequencies, f)

    logging.info("Getting co-occurrence number of company pairs from Google")
    competitor_names = list()
    for c1, c2 in list(zip(pair_company_ids1, pair_company_ids2)):
        if c1 not in company_frequencies:
            logging.error(f"{c1} does not have known name")
            continue
        if c2 not in company_frequencies:
            logging.error(f"{c2} does not have known name")
            continue

        comp1_name, f_w1 = company_frequencies[c1]
        comp2_name, f_w2 = company_frequencies[c2]

        competitor_names.append([comp1_name, c1, comp2_name, c2])
    frequency_of_couple = get_competitor_frequencies(gclient, competitor_names)

    with open(f"competitor_frequency_google_api_example.pickle", "wb") as f:
        pickle.dump(frequency_of_couple, f)
