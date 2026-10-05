# Year 12 Study Centre screen

A display for the TV in the Year 12 Study Centre. It runs by itself and needs no mouse or keyboard.

**Always on screen**
- The time and date.
- **Right now:** the current period (using the Mon–Thu or Friday bell times), time left, and a progress bar.
- **Focus timer:** 25 minutes of focus, then a 5-minute break, starting from the beginning of each lesson so the whole room works together.
- **Break Space:** shows Open at break and lunch and Closed at all other times, with when it next opens.
- **Along the bottom:** zone reminders and notices, plus the Gravesend weather, including whether rain is likely later.

**Panels that rotate every 20 seconds:** countdowns, the study technique of the day, who can help, a thought for the day, and notices.

**Outside school hours** (before 07:45, after 16:30, at weekends, on holidays and development days) it shows a dim clock with "See you tomorrow" or "Enjoy the holiday! Back in school on …".

**At break and lunch**, the video-free news card rotates BBC News headlines every 14 seconds. The current story can be opened from the card. The screen reads `news.json` from this same site, so the display device does not need access to YouTube or a third-party news API. A scheduled GitHub Action refreshes the file four times on school days; the displayed timestamp makes delayed updates clear. The screen can use a recent local copy if a request fails and shows a neutral unavailable message if that copy is too old.

## Editing the content

School information is in **`content.txt`**. You edit it on the GitHub website: open the file, click the pencil icon, make your change, then click **Commit changes**. The screen picks up changes within 15 minutes. BBC headlines are updated automatically in `news.json`.

- Bell times, term dates, countdowns, support contacts, notices and zone reminders are all in that file, with instructions at the top.
- The next countdown is always the big number. Marking one `big` (like the Prep Exams) keeps it listed underneath even when it's months away.
- Past countdowns disappear by themselves.
- About 30 study tips and 25 thoughts for the day are built in. Add your own under `# MY TIPS` and `# MY QUOTES`.
- If a line is typed wrongly, the screen skips that line instead of breaking.

**Preview it out of hours** by adding `?preview` to the end of the address. This shows the next weekday at 10:30.

**Preview any date and time** by adding `?now=` to the address, for example:
- `…/?now=2026-10-07T10:30`: a Wednesday lesson
- `…/?now=2026-10-09T11:40`: Friday break
- `…/?now=2026-10-28T10:00`: half term

## Setup

1. Create a GitHub repository, for example `study-centre-screen`, and upload these files.
2. Go to **Settings → Pages**, set Source to **Deploy from a branch**, choose `main` and `/ (root)`, then save. The address will be `https://<your-username>.github.io/study-centre-screen/`.
3. Give that address to IT.

## Notes for IT

- It's a single static web page with no login, cookies or tracking. The screen itself requests only its own site and weather from api.open-meteo.com; a GitHub Action fetches the BBC feed separately.
- Open the address full screen. On a PC use Chrome or Edge kiosk mode, e.g. `msedge --kiosk <url> --edge-kiosk-type=fullscreen`. On a smart TV, use the built-in browser's full-screen option. On a signage player, add it as a web page or URL item.
- It's designed at 1920×1080 and scales to fit any screen size. It's lightweight enough for smart-TV browsers.
- It reloads itself at 06:00 every day and checks for content changes every 15 minutes. If the network drops, it keeps showing what it has.
- Every few minutes everything shifts by a few pixels, and out of hours it goes to a dim clock, to reduce screen burn-in. If the TV can be scheduled to switch off out of hours, that's even better.
