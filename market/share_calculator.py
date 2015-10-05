
def share_smallerQualityFirst(q1,q2,p1,p2,alpha):
    share1 = max(min((float(p2 - p1) / float(q2 - q1))/float(alpha),1),0)
    print share1
    share2 = 1 - share1
    return share1, share2


def calculator(q1,q2,p1,p2,alpha):
    if q1 < q2:
        share1, share2 = share_smallerQualityFirst(q1,q2,p1,p2,alpha)
    elif q1 > q2:
        share2, share1 = share_smallerQualityFirst(q1,q2,p1,p2,alpha)
    else:
        if p1 > p2:
            share1, share2 = 0, 1
        elif p1 < p2:
            share1, share2 = 1, 0
        else:
            share1, share2 = 0.5, 0.5

    return share1, share2