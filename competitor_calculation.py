from google_similarity import PMID, NGD, number_of_results
import pickle
import pandas as pd


if __name__ == '__main__':

    all_companies_frequencies = dict()
    for i in range(9):
        s = i*200
        e = s + 200
        f = open(f"company_frequencies_{s}_{e}_2.pickle", "rb")
        data = pickle.load(f)
        all_companies_frequencies = {**data, **all_companies_frequencies}
    print(len(all_companies_frequencies.items()))

    all_competitors_frequencies = dict()
    for i in range(5):
        s = i * 200
        e = s + 200
        f = open(f"competitor_frequency_{s}_{e}.pickle", "rb")
        data = pickle.load(f)
        all_competitors_frequencies = {**data, **all_competitors_frequencies}
    print(len(all_competitors_frequencies.items()))

    D = number_of_results("the")
    print(D)

    df_dict = {"comp1": [], "comp2": [], "comp1 name": [], "comp2 name": [], "google similarity score": [],
               "document-based PMI": []}

    for (comp1, comp2), d_w1_dw2 in all_competitors_frequencies.items():
        comp1_name, d_w1 = all_companies_frequencies[comp1]
        comp2_name, d_w2 = all_companies_frequencies[comp2]

        df_dict["comp1"].append(comp1)
        df_dict["comp2"].append(comp2)
        df_dict["comp1 name"].append(comp1_name)
        df_dict["comp2 name"].append(comp2_name)

        google_score = NGD(d_w1, d_w2, d_w1_dw2, D)
        pmi = PMID(d_w1, d_w2, d_w1_dw2, D)

        df_dict["google similarity score"].append(google_score)
        df_dict["document-based PMI"].append(pmi)

    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv("competitor_scores_pmi_and_google.csv")
