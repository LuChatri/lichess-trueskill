# Lichess TrueSkill
Applying Microsoft's [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) rating system to chess games from [database.lichess.org](https://www.database.lichess.org/).
## Installation
To install, clone this repo.

`git clone https://github.com/LuChatri/lichess-trueskill.git`

Install 3rd-party libraries using pip.

`pip install -r requirements.txt`

## Usage
Run `lichess_ts.py` from the command line.

```
>>>python lichess_ts.py -h
usage: lichess_ts.py [-h] [-m M] [-s S] [-b B] [-t T] [-d D] path

Rate PGNs using TrueSkill

positional arguments:
  path            Path to a Lichess PGN archive or folder of archives in the format used at database.lichess.org

optional arguments:
  -h, --help      show this help message and exit
  -m M, -mu M     Mu for TrueSkill ratings
  -s S, -sigma S  Sigma for TrueSkill ratings
  -b B, -beta B   Beta for TrueSkill ratings
  -t T, -tau T    Tau for TrueSkill ratings
  -d D, -draw D   Draw probability for TrueSkill ratings
```

If `lichess_ts.py` is run with the path to a PGN archive (e.g. `python lichess_ts.py -p C:\Path\To\lichess_db_antichess_rated_2020-10.pgn`) it will calculate TrueSkill ratings for every PGN in the file and write them back into the file.  For example:

```
...
[Event "Rated Antichess tournament https://lichess.org/tournament/guQXTwiM"]
[Site "https://lichess.org/Mw6h6QXG"]
[Date "2020.10.01"]
[Round "-"]
[White "JackDanielsHoney"]
[Black "sovok70"]
[Result "1-0"]

1. c4 { [%clk 0:01:30] } g6 { [%clk 0:01:30] } 2. g3 { [%clk 0:01:28] } b5 { [%clk 0:01:28] } 3. cxb5 { [%clk 0:01:28] } Bh6 { [%clk 0:01:26] } 4. b6 { [%clk 0:01:27] } cxb6 { [%clk 0:01:26] } 5. Bg2 { [%clk 0:01:19] } Bxd2 { [%clk 0:01:24] } 6. Bxa8 { [%clk 0:01:19] } Bxc1 { [%clk 0:01:21] } 7. Qxd7 { [%clk 0:01:19] } Bxb2 { [%clk 0:01:19] } 8. Qxd8 { [%clk 0:01:19] } Bxa1 { [%clk 0:01:18] } 9. Qxe7 { [%clk 0:01:17] } Kxe7 { [%clk 0:01:15] } 10. Nc3 { [%clk 0:01:15] } Bxc3 { [%clk 0:01:14] } 11. Kd2 { [%clk 0:01:12] } Bxd2 { [%clk 0:01:14] } 12. Bb7 { [%clk 0:01:08] } Bxb7 { [%clk 0:01:13] } 13. a4 { [%clk 0:01:07] } Bxh1 { [%clk 0:01:12] } 14. e4 { [%clk 0:01:07] } Bxe4 { [%clk 0:01:11] } 15. Nf3 { [%clk 0:01:02] } Bxf3 { [%clk 0:01:10] } 16. g4 { [%clk 0:01:01] } Bxg4 { [%clk 0:01:09] } 17. h3 { [%clk 0:01:01] } Bxh3 { [%clk 0:01:08] } 18. f4 { [%clk 0:01:01] } 1-0
...
```

becomes

```
...
[Event "Rated Antichess tournament https://lichess.org/tournament/guQXTwiM"]
[Site "https://lichess.org/Mw6h6QXG"]
[Date "2020.10.01"]
[Round "-"]
[White "JackDanielsHoney"]
[Black "sovok70"]
[Result "1-0"]
[WhiteMu "25.0"]
[WhiteSigma "8.333333333333334"]
[WhiteNewMu "29.39583201999916"]
[WhiteNewSigma "7.171475587326195"]
[BlackMu "25.0"]
[BlackSigma "8.333333333333334"]
[BlackNewMu "20.604167980000835"]
[BlackNewSigma "7.171475587326195"]

1. c4 { [%clk 0:01:30] } g6 { [%clk 0:01:30] } 2. g3 { [%clk 0:01:28] } b5 { [%clk 0:01:28] } 3. cxb5 { [%clk 0:01:28] } Bh6 { [%clk 0:01:26] } 4. b6 { [%clk 0:01:27] } cxb6 { [%clk 0:01:26] } 5. Bg2 { [%clk 0:01:19] } Bxd2 { [%clk 0:01:24] } 6. Bxa8 { [%clk 0:01:19] } Bxc1 { [%clk 0:01:21] } 7. Qxd7 { [%clk 0:01:19] } Bxb2 { [%clk 0:01:19] } 8. Qxd8 { [%clk 0:01:19] } Bxa1 { [%clk 0:01:18] } 9. Qxe7 { [%clk 0:01:17] } Kxe7 { [%clk 0:01:15] } 10. Nc3 { [%clk 0:01:15] } Bxc3 { [%clk 0:01:14] } 11. Kd2 { [%clk 0:01:12] } Bxd2 { [%clk 0:01:14] } 12. Bb7 { [%clk 0:01:08] } Bxb7 { [%clk 0:01:13] } 13. a4 { [%clk 0:01:07] } Bxh1 { [%clk 0:01:12] } 14. e4 { [%clk 0:01:07] } Bxe4 { [%clk 0:01:11] } 15. Nf3 { [%clk 0:01:02] } Bxf3 { [%clk 0:01:10] } 16. g4 { [%clk 0:01:01] } Bxg4 { [%clk 0:01:09] } 17. h3 { [%clk 0:01:01] } Bxh3 { [%clk 0:01:08] } 18. f4 { [%clk 0:01:01] } 1-0
...
```

## Performance
This code takes three minutes to rank ~370,000 Antichess Lichess games on my mid-range laptop.  Most of this time lies in the TrueSkill library, so there's little I can do to improve performance.  Extrapolating out to the ~70,000,000 standard chess games played on Lichess last month, this program would run for about 9.5 hours.  Memory efficiency is decent.  The code backs up the file it is reading to disk in case it is interrupted (a very good thing).  Unfortunately, this means it temporarily doubles the disk space occupied by the dataset being ranked, which in the case of Lichess archives can translate to tens of Gigabytes of extra space.

