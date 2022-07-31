"""
Plotting.py

Helper to plot things.
"""

import matplotlib.pyplot as plt

import pandas as pd


def l(obj):
    result = [0, 0, 0, 0, 0]
    for item in obj:
        result[item - 1] += 1
    total = sum(result)
    for idx in range(len(result)):
        result[idx] = 100.0 * result[idx] / total
    return result


if __name__ == '__main__':
    local_g1 = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5])
    local_g2 = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5])
    local_g3 = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
    local_s = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5])
    local_f = l([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])

    global_g1 = l([1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5])
    global_g2 = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5])
    global_g3 = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5])
    global_s = l([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5])
    global_f = l([1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])

    empty = [0] * 5

    likert_colors = ['white', 'firebrick', 'lightcoral', 'gainsboro', 'cornflowerblue', 'darkblue']
    dummy = pd.DataFrame(
        [local_g1, global_g1, empty, local_g2, global_g2, empty, local_g3, global_g3, empty, local_s, global_s, empty,
         local_f, global_f],
        columns=["SD", "D", "N", "A", "SA"],
        index=["Loc-G#1", "Gbl-G#1", "",
               "Loc-G#2", "Gbl-G#2", "",
               "Loc-G#3", "Gbl-G#3", "",
               "Loc-Sat", "Gbl-Sat", "",
               "Loc-Fru", "Gbl-Fru",
               ])
    middles = dummy[["SD", "D"]].sum(axis=1) + dummy["N"] * .5
    longest = middles.max()
    longest = int(longest * 1.1)
    complete_longest = dummy.sum(axis=1).max()
    dummy.insert(0, '', (middles - longest).abs())

    dummy.plot.barh(stacked=True, color=likert_colors, edgecolor='none', legend=False)
    z = plt.axvline(longest, linestyle='--', color='black', alpha=.5)
    z.set_zorder(-1)

    complete_longest = int(complete_longest * 1.5)

    plt.xlim(0, complete_longest)
    xvalues = range(0, complete_longest, 10)
    xlabels = [str(x - longest) for x in xvalues]
    plt.xticks(xvalues, xlabels)
    # _,ax = plt.subplots()
    # ax.yaxis.grid(True,which="major")
    plt.xlabel("% (Right-hand side for Agreeing)")
    plt.title("Exit Survey results (Likert Scale)")

    plt.legend()

    plt.show()
