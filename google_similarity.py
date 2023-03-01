import math


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
    if f_w1 <= 0 or f_w2 <= 0 or f_w1_w2 < 0:
        return -10000
    if f_w1_w2 == 0:
        return 10000

    f_w1 = math.log(f_w1, 2)
    f_w2 = math.log(f_w2, 2)
    f_w1_w2 = math.log(f_w1_w2, 2)
    return (max(f_w1, f_w2) - f_w1_w2) / (N - min(f_w1, f_w2))
