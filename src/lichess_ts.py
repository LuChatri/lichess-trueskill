import argparse
import collections
import fileinput
import os
import os.path
import re
import trueskill


HERE = os.path.dirname(os.path.realpath(__file__))
DEFAULT_DIR = HERE
DEFAULT_MU = 25
DEFAULT_SIGMA = DEFAULT_MU / 3
DEFAULT_BETA = DEFAULT_SIGMA / 2
DEFAULT_TAU = DEFAULT_SIGMA / 100
DEFAULT_DRAW_PROB = 0.1


class PathAction(argparse.Action):
    
    def __call__(self, parser, namespace, values, options, option_string=None):
        if not (os.path.isdir(values) or os.path.isfile(values)):
            raise argparse.ArgumentError(self, 'path to data must be file or dir')
        setattr(namespace, self.dest, values)


class DrawAction(argparse.Action):
    
    def __call__(self, parser, namespace, values, options, option_string=None):
        if not 0 <= values <= 1:
            raise argparse.ArgumentError(self, 'draw probability must be in range 0-1')
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(description='Rate PGNs using TrueSkill')
parser.add_argument('-p', '-path',
                    help='Path to a Lichess PGN archive or folder of archives in the format used at database.lichess.org',
                    default=DEFAULT_DIR,
                    action=PathAction)
parser.add_argument('-m', '-mu',
                    help='Mu for TrueSkill ratings',
                    default=DEFAULT_MU,
                    type=float,)
parser.add_argument('-s', '-sigma',
                    help='Sigma for TrueSkill ratings',
                    default=DEFAULT_SIGMA,
                    type=float)
parser.add_argument('-b', '-beta',
                    help='Beta for TrueSkill ratings',
                    default=DEFAULT_BETA,
                    type=float)
parser.add_argument('-t', '-tau',
                    help='Tau for TrueSkill ratings',
                    default=DEFAULT_TAU,
                    type=float)
parser.add_argument('-d', '-draw',
                    help='Draw probability for TrueSkill ratings',
                    default=DEFAULT_DRAW_PROB,
                    type=float,
                    action=DrawAction)


def main(path):
    # Currently, this program writes no temp information to the disk,
    # so the cache includes current ratings for all players being
    # rated.  It could get large, but if you're working with
    # a dataset with tens of millions of players, you probably have
    # a few GB of RAM to spare.  I expect ~300MB to be used for 10M
    # players, so it shouldn't matter.
    cache = collections.defaultdict(trueskill.Rating)
    
    # Verification of path already occurred.
    # Path is to a file or directory of newline-separated
    # chess games in PGN format.
    if os.path.isdir(path):
        files =  list(sorted(os.path.abspath(p) for p in os.listdir(path)
                             if os.path.isfile(p)))
    else:
        files = [path]

    template = '{}' \
               '[WhiteMu "{}"]\n' \
               '[WhiteSigma "{}"]\n' \
               '[WhiteNewMu "{}"]\n' \
               '[WhiteNewSigma "{}"]\n' \
               '[BlackMu "{}"]\n' \
               '[BlackSigma "{}"]\n' \
               '[BlackNewMu "{}"]\n' \
               '[BlackNewSigma "{}"]\n' \
               '{}'
    with fileinput.input(files=files, inplace=True, backup='.bak') as f:
        pgn_headers = ''
        pgn_moves = ''
        
        for line in f:
            if line.startswith('[Event'):
                # A new PGN is starting.
                if pgn_headers:
                    out = rate_pgn(pgn_headers, cache)
                    if out is not None:
                        wo, wn, bo, bn = out
                        pgn = template.format(pgn_headers, wo.mu, wo.sigma, wn.mu,
                                              wn.sigma, bo.mu, bo.sigma, bn.mu,
                                              bn.sigma, pgn_moves)
                        print(pgn)
                pgn_headers = ''
                pgn_moves = ''
            elif line.startswith('['):
                pgn_headers += line
            else:
                pgn_moves += line


def rate_pgn(pgn, cache):
    # No need to re.compile since we only use a few regexes.
    fields = [re.search(r'\[White "(.*)"\]', pgn),
              re.search(r'\[Black "(.*)"\]', pgn),
              re.search(r'\[Result "(.*)"\]', pgn)]
    if None in fields:
        # Missing Information
        return
    else:
        fields = [i.group(1) for i in fields]

    white, black, scores = fields
    # TrueSkill expects ranks (lower is better).
    # Lichess gives scores (higher is better).
    # Reversing scores converts them into ranks.
    try:
        scores = scores.split('-')
        ranks = (float(scores[1]), float(scores[0]))
    except ValueError:
        # Incorrectly Formatted PGN
        return

    wr = cache[white]
    br = cache[black]
    old = ((wr, ), (br, ))
    # trueskill.rate() expects and returns rating tuples, not ratings
    new = list(r[0] for r in trueskill.rate(old, ranks=ranks))

    # Update the cache
    for user, rating in zip([white, black], new):
        cache[user] = rating

    return wr, br, new[0], new[1]



if __name__ == '__main__':
    args = parser.parse_args()
    trueskill.setup(mu=args.m, sigma=args.s, beta=args.b,
                    tau=args.t, draw_probability=args.d)
    main(args.p)
