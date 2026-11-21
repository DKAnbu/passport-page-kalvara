[![make.fun](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/DKAnbu/passport-page-kalvara/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/DKAnbu/passport-page-kalvara/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

# Passport Page of Kalvara

An open passport spread for the **Republic of Kalvara** — a fictional
salt-island republic whose capital is Port Saline — built for the
[make.fun bounty "The Passport Page of a Country That Isn't There"](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318).

The data page shows holder Mara Selin Voss (passport KLV 482 913, issued
12 Mar 2023 in Port Saline, valid to 12 Mar 2033), a stylised PIL-drawn
portrait, and an ICAO 9303 machine-readable zone with correct check digits.
The visas page carries five entry/exit stamps from neighbouring Tarnovia,
Ostara and Meridian Free Port, all dated 2024–2026 — none before the
passport's issue — plus the telling paperwork detail: a red visa-condition
stamp, *"Holder may not enter the salt flats without a guide permit —
Art. 7"*.

## Run

```sh
python3 main.py            # writes out/entry.png (1024x680, < 1 MiB)
python3 draw_image.py      # redraw entry.png from scratch (needs Pillow)
```

`main.py` uses only the Python standard library and needs no network: it
copies the pre-drawn `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `out`).

Everything in the image — portrait, coat of arms, guilloche, stamps — is
drawn with Pillow shapes and text. No external images are used.
