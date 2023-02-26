from google_similarity import number_of_results


frequencies = dict()
import random, time
import pickle
import pandas as pd


def sleep(alpha, beta):
    """Sleep for an amount of time in range(alpha, beta)"""
    rand = random.Random()
    time.sleep(0.5)


from argparse import ArgumentParser

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-s", "--start", default="1600")
    parser.add_argument("-e", "--end", default="1800")

    args = parser.parse_args()
    df = pd.read_csv("/Users/edacicek/Downloads/1k-to-triple-labeled-majority-hashed.csv")

    company_ids1 = df["ID1"].tolist()
    company_ids2 = df["ID2"].tolist()

    print(len(company_ids2))
    # #
    # # google_scores = list()
    s = int(args.start)
    e = int(args.end)
    # print(len(company_ids1[s:e]))
    # # print(len(company_ids1[s:e]))
    # #
    # frequency_of_couple = dict()
    #
    # for i, (comp1, comp2) in enumerate(list(zip(company_ids1[s:e], company_ids2[s:e]))):
    #     print(i)
    #     if comp1 not in all_companies_frequencies or comp1 not in all_companies_frequencies:
    #         print("no names")
    #         print(comp1)
    #         print(comp2)
    #         print()
    #         continue
    #
    #     comp1_name, f_w1 = all_companies_frequencies[comp1]
    #     comp2_name, f_w2 = all_companies_frequencies[comp2]
    #     no_ = number_of_results(f"{comp1_name} {comp2_name}")
    #     frequency_of_couple[(comp1, comp2)] = no_
    #     # sleep(5, 10)
    #
    # with open(f"competitor_frequency_{s}_{e}.pickle", "wb") as f:
    #     pickle.dump(frequency_of_couple, f)

    with open("company_names.pickle", "rb") as f:
        names_ids = pickle.load(f)
        print(len(names_ids))

    for i, (name, id_) in enumerate(names_ids[s:e]):
        no_ = number_of_results(f"{name}")
        print(no_)
        frequencies[id_] = [name, no_]
        sleep(5, 10)

    with open(f"company_frequencies_{s}_{e}_2.pickle", "wb") as f:
        pickle.dump(frequencies, f)
