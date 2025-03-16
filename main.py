from argparse import ArgumentParser

from Cart_Pole import run_simulation

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")




group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--run', type=str, default="Q_table0_Z10L0G0.npy")

group_metrics = parser.add_mutually_exclusive_group()
group_metrics.add_argument('-m1', '--test_metric1', action="store_true")
group_metrics.add_argument('-m2', '--test_metric2', action="store_true")
group_metrics.add_argument('-m3', '--test_metric3', action="store_true")


group.add_argument('-t', '--train', action='store_true')

group_cut = parser.add_mutually_exclusive_group()
group_cut.add_argument('-cn', '--cut_not_zero', action='store_true')
group_cut.add_argument('-cc', '--cut_close_zero', action='store_true')

group_function = parser.add_mutually_exclusive_group()
group_function.add_argument("-l", "--linear", action="store_true")
group_function.add_argument("-g", "--geom", action="store_true")


if __name__ == '__main__':
    run_simulation(parser.parse_args())