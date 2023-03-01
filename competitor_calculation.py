from google_similarity import PMID, NGD
import pickle
import pandas as pd
import math

from argparse import ArgumentParser


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-pcf", "--path_to_company_frequencies",
                       default="company_frequencies_google_api_example.pickle")
    parser.add_argument("-ppf", "--path_to_pair_frequencies",
                        default="competitor_frequency_google_api_example.pickle")
    args = parser.parse_args()

    with open(args.path_to_company_frequencies, "rb") as f:
        all_companies_frequencies = pickle.load(f)

    with open(args.path_to_pair_frequencies, "rb") as f:
        all_competitors_frequencies = pickle.load(f)

    D = 49490000000.0

    df_dict = {"comp1": [], "comp2": [], "comp1 name": [], "comp2 name": [], "google similarity score": [],
               "comp1 frequency": [], "comp2 frequency": [], "pair frequency": []}

    for (comp1, comp2), d_w1_dw2 in all_competitors_frequencies.items():
        comp1_name, d_w1 = all_companies_frequencies[comp1]
        comp2_name, d_w2 = all_companies_frequencies[comp2]

        df_dict["comp1 frequency"].append(d_w1)
        df_dict["comp2 frequency"].append(d_w2)
        df_dict["pair frequency"].append(d_w1_dw2)

        df_dict["comp1"].append(comp1)
        df_dict["comp2"].append(comp2)
        df_dict["comp1 name"].append(comp1_name)
        df_dict["comp2 name"].append(comp2_name)

        google_score = NGD(d_w1, d_w2, d_w1_dw2, D)

        df_dict["google similarity score"].append(google_score)

    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv("competitor_scores_pmi_and_gsd_example.csv")
