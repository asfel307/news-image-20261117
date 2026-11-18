# The World in One Day — Tuesday, 17 November 2026

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/asfel307/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/asfel307/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

An entry for the [make.fun bounty "Sum up 17 November's world news in one image"](https://make.fun/bounty/news-image-20261117): a 1024×1024 front-page infographic of Tuesday 17 November 2026, drawn programmatically with PIL so every letter is crisp.

## The day's news

- **Lead — the Gulf:** US fighter jets strike an Iranian missile launch site on Qeshm Island, in retaliation after Iran targeted US forces; Iranian drones hit a US radar in Bahrain, and the tanker Tara Gas is struck in the Strait of Hormuz with 24 crew rescued (Reuters, 17 Nov).
- **War — Ukraine:** Ukraine hits the Kerch Bridge for a second straight day and a road span collapses into the water; Russia strikes bridges in Kyiv (CNN, 17 Nov).
- **Asia — diplomacy:** Trump arrives in Manila for his first Quad summit since returning to office, then heads to Shenzhen for APEC (AP, 17 Nov).
- **Europe — airspace:** Japan scrambles fighter jets after two suspected Russian aircraft enter its airspace; Tokyo lodges a formal protest with Moscow (17 Nov).
- **Health — USA:** The US loses its measles elimination status, the first loss since 2000, after 12 months of uninterrupted transmission (PAHO, 17 Nov).
- **Aid — Gaza:** The UK, Australia, Canada and Italy urge Israel to open Gaza crossings as winter rains flood shelters (UN, 17 Nov).

Every story was reported on Tuesday 17 November 2026; sources are listed on the image itself.

## How to run

```sh
# Re-draw the image (needs Pillow, only for the build step):
python3 render.py

# The entry program (Python 3.13, standard library only):
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` copies the repository's `entry.png` to the output directory, so both grading runs write identical bytes. The image is a whole PNG, 1024×1024, under 1 MiB.

## License

MIT — see [LICENSE](LICENSE).
