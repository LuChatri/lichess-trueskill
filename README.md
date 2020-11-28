# Lichess TrueSkill
Applying Microsoft's [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) rating system to chess games from [database.lichess.org](https://www.database.lichess.org/).
## Installation
To install, clone this repo.

`git clone https://github.com/LuChatri/lichess-trueskill`

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

1. c4 { [%clk 0:01:30] } ... 18. f4 { [%clk 0:01:01] } 1-0
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

1. c4 { [%clk 0:01:30] } ... 18. f4 { [%clk 0:01:01] } 1-0
...
```

## And Now for Something Different
I rated the last month (Oct. 2020) of Antichess results.  Here are my findings.
### Top Antichess Players
| Player | Max Mu | Sigma at Max Mu | Chance of Beating VariantsBot
| --- | --- | --- | ---
VariantsBot (Bot) | 52.6159 | 1.7498 | 50%
PinChampKexGasm (Banned) | 49.6982 | 1.875 | 12.763%
Disconnectattack (Banned) | 45.895 | 2.3481 | 1.086%
XXIstCentury (Bot) | 45.7471 | 2.3138 | 0.895%
Teilchen | 45.3695 | 2.0685 | 0.374%
MrHaggis | 44.6572 | 3.2738 | 1.602%
lo-ol | 44.574 | 3.2804 | 1.527%
rrrrrrrrrrrroooo | 44.3997 | 2.4119 | 0.291%
trashcan_man | 44.2671 | 3.2711 | 1.221%
AdamBachtiar_PCTR | 44.1157 | 2.6517 | 0.373%

### Highest Rated Matchup
XXIstCentury (45) vs VariantsBot (53)

### Lowest Rated Matchup
matito (6) vs CaptainCadocaps (6)

## Performance
This code takes three minutes to rank ~370,000 Antichess Lichess games on my mid-range laptop.  Most of this time lies in the TrueSkill library, so there's little I can do to improve performance.  Extrapolating out to the ~70,000,000 standard chess games played on Lichess last month, this program would run for about 9.5 hours.  Memory efficiency is decent.  The code backs up the file it is reading to disk in case it is interrupted (a very good thing).  Unfortunately, this means it temporarily doubles the disk space occupied by the dataset being ranked, which in the case of Lichess archives can translate to tens of Gigabytes of extra space.
