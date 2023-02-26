import pandas as pd


if __name__ == '__main__':
    df_comp = pd.read_csv("competitor_scores_pmi_and_google.csv")
    google_scores = df_comp["google similarity score"].tolist()
    pmi_scores = df_comp["document-based PMI"].tolist()
    comp1s = df_comp["comp1"].tolist()
    comp2s = df_comp["comp2"].tolist()

    scores_all = dict()
    for i, (c1, c2) in enumerate(list(zip(comp1s, comp2s))):
        scores_all[(c1, c2)] = [google_scores[i], pmi_scores[i]]

    top_1k_pairs = dict()

    df = pd.read_csv("/Users/edacicek/Downloads/non-acquired-pairs.csv")

    comp1 = df['Column_1'].tolist()
    comp2 = df['Column_2'].tolist()
    labels = df['Column_3'].tolist()

    for i, c1 in enumerate(comp1):
        try:
            top_1k_pairs[(c1, comp2[i])] = labels[i]
        except Exception:
            print(c1)

    thresholds_google = [0.1, 0.25, 0.4, 0.6, 0.75, 1, 1.5]
    thresholds_pmi = [1, 2, 3, 5, 6, 7, 9]

    def f1(precision, recall):
        return 2 * (precision * recall) / (precision + recall)

    results = {"tp": [], "tn": [], "fp": [], "fn": [], "precision": [],
               "recall": [], "f1": [], "threshold": []}

    results_pmi = {"tp": [], "tn": [], "fp": [], "fn": [], "precision": [],
               "recall": [], "f1": [], "threshold": []}

    for i in range(len(thresholds_google)):
        tp, fp, tn, fn = 0, 0, 0, 0
        tp_pmi, fp_pmi, tn_pmi, fn_pmi = 0, 0, 0, 0
        for (c1, c2), label in top_1k_pairs.items():
            gscore, pscore = scores_all[(c1, c2)]
            if gscore > 0 and gscore < thresholds_google[i]:
                if label:
                    tp += 1
                else:
                    fp += 1
            else:
                if label:
                    fn += 1
                else:
                    tn += 1

            if pscore > 0 and pscore > thresholds_pmi[i]:
                if label:
                    tp_pmi += 1
                else:
                    fp_pmi += 1
            else:
                if label:
                    fn_pmi += 1
                else:
                    tn_pmi += 1

        results["tp"].append(tp)
        results["tn"].append(tn)
        results["fp"].append(fp)
        results["fn"].append(fn)
        results["precision"].append(tp / (tp + fp))
        results["recall"].append(tp / (tp + fn))
        results["f1"].append(f1(tp / (tp + fp), tp / (tp + fn)))
        results["threshold"].append(thresholds_google[i])

        results_pmi["tp"].append(tp_pmi)
        results_pmi["tn"].append(tn_pmi)
        results_pmi["fp"].append(fp_pmi)
        results_pmi["fn"].append(fn_pmi)
        results_pmi["precision"].append(tp_pmi / (tp_pmi + fp_pmi))
        results_pmi["recall"].append(tp_pmi / (tp_pmi + fn_pmi))
        results_pmi["f1"].append(f1(tp_pmi / (tp_pmi + fp_pmi), tp_pmi / (tp_pmi + fn_pmi)))
        results_pmi["threshold"].append(thresholds_pmi[i])

    import pandas as pd

    df = pd.DataFrame.from_dict(results)
    df.to_csv("google_score_results.csv")

    df = pd.DataFrame.from_dict(results_pmi)
    df.to_csv("pmi_score_results.csv")
