import pandas as pd
from argparse import ArgumentParser


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-path_to_company_pairs", "--pair_names_path")
    args = parser.parse_args()

    df_comp = pd.read_csv("competitor_scores_pmi_and_gsd_example.csv")
    google_scores = df_comp["google similarity score"].tolist()
    comp1s = df_comp["comp1"].tolist()
    comp2s = df_comp["comp2"].tolist()

    scores_all = dict()
    for i, (c1, c2) in enumerate(list(zip(comp1s, comp2s))):
        scores_all[(c1, c2)] = google_scores[i]

    top_1k_pairs = dict()

    df = pd.read_csv(args.pair_names_path)

    comp1 = df['ID1'].tolist()
    comp2 = df['ID2'].tolist()
    labels = df['Label'].tolist()

    positives = 0
    negatives = 0
    for i, c1 in enumerate(comp1):
        try:
            top_1k_pairs[(c1, comp2[i])] = labels[i]
            if labels[i]:
                positives += 1
            else:
                negatives += 1
        except Exception:
            print(c1)

    print(positives)
    print(negatives)

    print(positives/(positives+negatives))

    thresholds_google = [0.3, 0.4, 0.5, 0.6, 0.75, 0.9, 1.1]


    def f1(precision, recall):
        return 2 * (precision * recall) / (precision + recall)

    results = {"tp": [], "tn": [], "fp": [], "fn": [], "precision": [],
               "recall": [], "f1": [], "threshold": []}


    for i in range(len(thresholds_google)):
        print(i)
        tp, fp, tn, fn = 0, 0, 0, 0
        for (c1, c2), label in top_1k_pairs.items():
            gscore= scores_all[(c1, c2)]
            if gscore < thresholds_google[i]:
                if label:
                    tp += 1
                else:
                    fp += 1
            else:
                if label:
                    fn += 1
                else:
                    tn += 1

        results["tp"].append(tp)
        results["tn"].append(tn)
        results["fp"].append(fp)
        results["fn"].append(fn)
        results["precision"].append(tp / (tp + fp))
        results["recall"].append(tp / (tp + fn))
        results["f1"].append(f1(tp / (tp + fp), tp / (tp + fn)))
        results["threshold"].append(thresholds_google[i])

    df = pd.DataFrame.from_dict(results)
    df.to_csv("google_score_results_example.csv")
