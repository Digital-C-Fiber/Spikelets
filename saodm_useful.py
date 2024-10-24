##
# Date of change: July 10th, 2022

## -----------------------------------------------------------------------------------------------##
# Useful functions
## -----------------------------------------------------------------------------------------------##
# These functions are general enough to be called a various places troughout the code.
## -----------------------------------------------------------------------------------------------##


# basics
from numpy import mean, nan, sqrt, var
from pandas import read_csv


##
# @param
# @return
def calc_fano_factor(spikes_list: list, start_time: float, segment_lenght: float):
    current = start_time
    end_time = current + 480.
    arr = list()
    while(current + segment_lenght <= end_time):
        arr.append(len(list(filter(lambda x: current <= x and x < current + segment_lenght, spikes_list))))
        current += segment_lenght
    return var(arr) / mean(arr)



##
# @param
# @return
def calc_rr_sd1_sd2(isi_list: list):
    '''
    lines formula
    point p = (p1, p2)^T
    point c = (cc, cc)^T aka crosspoint of lines x1 and x2, also center of the ellipse
    line x1: c + lambda*b where b = (1, -1)^T => |b| = sqrt(2)
    line x2: c + lambda*b where b = (1, 1)^T => |b| = sqrt(2)
    sd1 stands on x2:
    d = |(p - c) x b| / |b|
        |(p1-cc, p2-cc) x (b1, b2)| / sqrt(2)
        |(p1-cc)(b2) - (p2-cc)(b1)| / sqrt(2) where b1 = 1, b2 = 1
        |(p1-cc) - (p2-cc)| / sqrt(2)
        |(p1-p2)| / sqrt(2)
    sd2 stand on x1:
    d = |(p1-cc)(b2) - (p2-cc)(b1)| / sqrt(2) where b1 = 1, b2 = -1
        |(p1-cc) + (p2-cc)| / sqrt(2)
        |(p1+p2-2cc)| / sqrt(2)
    '''
    cc = mean(isi_list)
    sd1, sd2 = 0., 0.

    sd1entries = list()
    sd2entries = list()
    for i in range(len(isi_list)-1):
        x, y = isi_list[i], isi_list[i+1]
        sd1entries.append((x - y) / sqrt(2))
        sd2entries.append((x + y - 2*cc) / sqrt(2))

    if len(sd1entries) > 0:
        sd1 = sqrt(var(sd1entries))
        sd2 = sqrt(var(sd2entries))
    return (cc, sd1, sd2)



##
# @param
# @return (regularity list, length list)
def calc_spikelets(isi_list: list):
    '''
    '''
    if len(isi_list) < 2:
        return []

    spikelets = list()   # 1 spikelet consist of 2 ISIs
    for x in range(len(isi_list)-1):
        spikelets += [(isi_list[x], isi_list[x+1])]

    return spikelets



##
# @param
# @return (regularity list, length list)
def calc_spikelet_regularity_and_length(isi_list: list):
    '''
    '''
    if len(isi_list) < 2:
        return ([nan], [nan])

    spikelets = list()   # 1 spikelet consist of 2 ISIs
    for x in range(len(isi_list)-1):
        spikelets += [(isi_list[x], isi_list[x+1])]

    # If x (left) is bigger than y (right), then y/x < 1.0 and therefor on the left side.
    # Alternatively use y-x, but change the plot funktion as well!
    spikelets_regularity = [y/x for (x, y) in spikelets]
    spikelets_length = [x+y for (x, y) in spikelets]
    return (spikelets_regularity, spikelets_length)



##
# @param
# @return
def read_csv_columns(file_name: str, captions: list):
    '''
    '''
    ret = dict()
    columns = read_csv(file_name, delimiter=';')

    for x in captions:
        ret[x] = list(columns[x])

    return ret

