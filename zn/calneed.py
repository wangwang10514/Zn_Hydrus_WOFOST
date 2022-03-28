def cal_ZDMI(j, blossom, MIZRT, MIZST, MIZLF, MIZER, WRT, WST, WLF, WER, ZART, ZAST, ZALF, ZAER):
    if j <= blossom:
        ZDMIRT = max(0, MIZRT * WRT - ZART)
        ZDMIST = max(0, MIZST * WST - ZAST)
        ZDMILF = max(0, MIZLF * WLF - ZALF)
        ZDMIER = max(0, MIZER * WER - ZAER)
    else:
        ZDMIRT = 0
        ZDMIST = 0
        ZDMILF = 0
        ZDMIER = max(0, MIZER * WER - ZAER)

    return ZDMIRT, ZDMIST, ZDMILF, ZDMIER


def cal_massfraction(ZA, W):
    if W != 0:
        ZMA = ZA / W
    else:
        ZMA = 0
    return ZMA


def cal_ZDU(j, blossom, ZDMIRT, ZDMIST, ZDMILF, ZDMIER, ZRT, ZST, ZLF, ZER):
    if j <= blossom:
        ZDURT = max(0, ZDMIRT - ZRT)
        ZDUST = max(0, ZDMIST - ZST)
        ZDULF = max(0, ZDMILF - ZLF)
        ZDUER = max(0, ZDMIER - ZER)
    else:
        ZDURT = 0
        ZDUST = 0
        ZDULF = 0
        ZDUER = max(0, ZDMIER - ZER)
    return ZDURT, ZDUST, ZDULF, ZDUER
