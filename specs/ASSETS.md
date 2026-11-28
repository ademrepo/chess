# ASSETS — where every asset comes from

Rule of the project: **no file is added to `specs/assets/` without a line in this table**
(author, source URL, licence, date, how it was obtained). Nothing comes from chess.com.

## Files in the project

| File | What it is | Author | Source | Licence | Obtained |
|------|------------|--------|--------|---------|----------|
| `specs/assets/pieces/wN.svg` | White knight (cburnett set) | Colin M.L. Burnett | https://github.com/lichess-org/lila/blob/master/public/piece/cburnett/wN.svg | GPLv2+ | 2026-11-20, `curl` of the raw file, 648 bytes |
| `specs/assets/pieces/bN.svg` | Black knight (cburnett set) | Colin M.L. Burnett | https://github.com/lichess-org/lila/blob/master/public/piece/cburnett/bN.svg | GPLv2+ | 2026-11-20, `curl` of the raw file, 837 bytes |
| `assets/ui.png` | Wooden UI sheet (board, panels, buttons) of the first replay screen; **no longer used by the code**: the wooden look is now drawn by `gui/wood.py`, the colours were sampled on this sheet | TO FILL IN | TO FILL IN | TO FILL IN | TO FILL IN |
| `assets/cat_sprite.png` | Cat sprite sheet (idle frames, 3 directions), used by `gui/cat.py` (the piece of the style "Cavalier Jack") | TO FILL IN | TO FILL IN | TO FILL IN | TO FILL IN |

**The two rows above come from the `adem` branch, where no source was written down: fill them in
(author, URL, licence, date) before handing in.**

SHA-256 of the files as downloaded (to prove they were not modified):

```
43d8bed9cd40836335072a20f52d30237e6e2cbe304ffb13e258fa1d576c156a  wN.svg
72e1565fbc9024015dcb6ee28d918c876523119f6f552c0a40d3118c13a67e13  bN.svg
a8ac1bd83665edf0a04f744cdb3b15c1073d8841e153b1ef2d95fb260b481df1  ui.png
514e8af1dfb96288e21d7d6ccbc5d8b02e52c737a6cafc296af694a15f4263cc  cat_sprite.png
```

## Licence proof

The licence and the author of the set are written in the Lichess repository, file
https://github.com/lichess-org/lila/blob/master/COPYING.md , line:

> `public/piece/cburnett | Colin M.L. Burnett (https://en.wikipedia.org/wiki/User:Cburnett) | GPLv2+`

GPLv2+ = GNU General Public License version 2 or later (https://www.gnu.org/licenses/gpl-2.0.txt).
The images are used **unmodified**. Only the white knight is used in the interface; the black knight
is kept for future use.

## Why this source

- Lichess (https://lichess.org) is an open-source chess server; its repository states the author and
  the licence of every image set, which makes the origin easy to verify.
- The pieces are vector files (SVG): pygame draws them at the exact size needed, so they stay sharp.
- chess.com's own pieces, board images and sounds are proprietary: **they were not downloaded, copied
  or traced.**

## What imitates chess.com (and what it does not copy)

| Element | How it is made |
|---------|----------------|
| Green and cream board, yellow highlight of visited squares | Plain colour values written in `gui/theme.py` (a colour is not a protected file) |
| Dark page, rounded 3D green buttons | Drawn by the code (`gui/widgets.py`) |
| Grey dots on the squares where the knight can go | Drawn by the code (`gui/game_screen.py`) |
| File letters a-h and ranks 1-8 in the board corners | Drawn by the code |
| Font | The system font (Segoe UI, falls back to Arial); no font file is shipped |

## Sounds

None. The project has no audio file.
