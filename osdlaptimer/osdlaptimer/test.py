def timeFromMillis(s):
    x1 = int(s) / 1000
    mmin = x1 / 60
    sec = x1 % 60
    hun = (int(s) % 1000) / 10
    
    print str(x1) + "," + str(mmin) + "," + str(sec) + "," + str(hun)
    ss = ""
    if mmin < 10:
        ss += "0"
    ss += str(mmin)
    ss += ":"
    if sec < 10:
        ss += "0"

    ss += str(sec)
    if hun < 10:
        ss += "0"
    ss += ":"
    ss += str(hun)
    return ss


print timeFromMillis("000000")