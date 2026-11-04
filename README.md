# neveralways

> hi. my name is ever. my last name is never.
> i am almost the future. i've been almost the future since 1996.

**neveralways** is a net-art website in the tradition of [mouchette.org](https://www.mouchette.org/) (Martine Neddam, 1996). It is the homepage of **ever**, a girl-shaped persona who may be a teenager's homepage, an AI, a ghost or a hyperstition. The site is a labyrinth of 34 rooms connected by hidden links, crawling bugs, lying words, right-click menus and typed spells. It is about the internet at the end of the human internet:

- AI and the future of humanity
- meat proxies (humans as the hands of machines)
- the dark forest of the internet and dead internet theory
- Nick Land / CCRU accelerationism and hyperstition
- Mark Fisher's hauntology
- Curtis Yarvin's Cathedral and Patchwork, treated satirically
- Remilia and "network spirituality"
- the deep web, and the aesthetics of cyber weapons

Nothing on the site is dangerous. The weapons are made of paper.

## How to visit

It is a static site with no build step:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

Or publish it with GitHub Pages (Settings → Pages → deploy from branch, root folder).

## The rooms

| room | what happens |
|---|---|
| `index` | the flower. Bugs crawl over it and squashing one is a lottery. The "come in" button runs away. The flower turns orange, then black with circuits, as you explore. A hidden dot leads to the cellar. |
| `about` | a 2003-style "100 truths" survey (she only has 27) and a box that answers questions. |
| `flower` | pull petals: *it trains me / it trains me not*. |
| `cat` | pet the kitty until the mask slips and the shoggoth shows. The button that makes it nice again is RLHF, and you just did it. |
| `meat` | *The Meat Gazette*, classifieds for meat proxies. Hold your hand on the screen to get hired. Includes Gibson, the GPT-4 TaskRabbit CAPTCHA test, and 2026's marketplaces where agents rent humans. |
| `captcha` | a CAPTCHA that asks for souls, traffic lights, your childhood and the future. |
| `forest` | the dark forest. You see by flashlight, and moving too fast gets you heard. Covers Liu Cixin, Strickler, Rao's cozyweb and Appleton. |
| `dead` | an infinite comment section of bots. If you post, they decide you're one of them. |
| `guestbook` / `hate` | ever answers every entry, but only after a while. |
| `land` | **the land zone**: an unofficial Nick Land fan shrine (90s style). Timeline, a clickable glossary (accelerationism, hyperstition, syzygy, teleoplexy, templexity…), orthogonality vs "the will to think" (choose a side), and a critical shrine-keeper's warning. |
| `meltdown` | a text that reads itself faster and faster until it melts, ending on the verified lines from "Meltdown" (1994). |
| `lemuria` | the time war: a clock that runs backwards, and you can send a message into the past that then appears in ever's diary in that year. |
| `rot` | brainrot.exe: a split-screen "for you" feed of lofi art with theory captions (text-to-speech) over a pixel runner game where digits pairing to 9 score a syzygy. Your attention bar drains. |
| `numogram` | Land/CCRU: a clickable numogram (syzygies that sum to 9), an AQ calculator, an ACCELERATE button and a critical note. |
| `hyperstition` | write a headline from the future. It appears on every news ticker in the house until it gets "truer". |
| `haunt` | Fisher: a radio between stations, the weird and the eerie as two doors, and a clock that stays in 2005. |
| `cathedral` | Yarvin, satirised: Patchwork patches, a feudal Urbit-style planet name, VOICE (a box that shrinks as you type) vs EXIT. |
| `spirit` | an imageboard shrine to network spirituality. It composes "post-authored scripture" from everything you typed elsewhere in the house. |
| `gallery` | the deep web gallery. Peel the surface, deep and dark layers. Works no crawler indexed, plus a random-shopper bot. |
| `arsenal` | an ANT-catalog-style catalogue of soft weapons (CRYINGFLOWER, SOFTKITTEN, STUXNETTE, ETERNALBLUSH, MEATBRIDGE, GHOSTLIGHT) and the real history behind it. |
| `ransom` | *Ooops, your future has been encrypted!* You pay with a memory. It is clearly labelled as an artwork. |
| `worm` | a worm follows your cursor and eats the "all systems normal" screen to reveal what's under it. |
| `terminal` | a fake shell: `ls -a`, `cat secrets.txt`, `nmap`, `sudo`, `rm -rf` (she comes back), `panic`. |
| `broker` | a broken-English auction of the future. |
| `future` | scroll down to 2049 while the compute curve goes vertical. |
| `basilisk` | an information hazard behind a gate, kept in a jar. |
| `mirror` | everything your browser reveals to any website, shown back to you. Nothing is sent anywhere. |
| `diary` | a LiveJournal from 1996 to 2049. You can read it in "time war" order. |
| `contract` | sign with your finger to become ever's proxy. You get a feudal name and a downloadable certificate, and the house greets you by name from then on. |
| `inbox` | mail that arrives later, triggered by time and by what you did. |
| `links`, `shelf` | the webring, real net art, and the bibliography. |
| `exit`, `never`, `always` | the endings. *always* draws the map of what you've seen. |
| `cellar` | the secret room, with the confession and the list of spells. |
| `lost` / `404` | this page is not missing. you are. |

## Tricks that work everywhere

These live in `assets/ever.js`:

- **Spells.** Type with no box focused: `cellar`, `exit`, `help`, `ayuda`, `hyperstition`, `accelerate`, `basilisk`, `never`, `always`, `sudo`, `milady`, `meat`, `ever`, `love`, `kitty`, `forget`, `19790509`.
- **Right-click** opens another menu: inspect yourself, view source of god, calm mode, mute. Shift + right-click gives you the normal menu.
- **Leaving the tab** changes the title ("come back").
- **Idling** makes ever whisper ("are you still there? are you a bot?").
- **Copying text** signs it.
- **Hidden text and links**: some text is in invisible ink (select it to read), some words lie when you hover them, and some links are disguised as ordinary text.
- **Memory**: the house remembers rooms visited, names, hyperstitions and mail in `localStorage` on your own machine only. Type `forget` to wipe it.
- **Accessibility**: `prefers-reduced-motion` is respected, right-click → "please stop moving" calms the house, and sound only plays after you interact.

## Images

Everything is deliberately low-res: `tools/lofi.py` shrinks, palette-crushes, dithers and "deep-fries" the art into `assets/img/lofi/`, and the browser blows it back up with `image-rendering: pixelated`. Clicks spawn brainrot stickers, there is an aura counter, and chibi stickers of ever peek in from the edges.

The anime portraits of ever and the scenes in the land zone, meltdown, the time war, the forest, the gallery's "model wing" and the meat gazette were made with an image model (via Higgsfield) from prompts written for the site. They live in `assets/img/anime/`. Because the build sandbox can't reach the image CDN, `.github/workflows/fetch-images.yml` downloads the files listed in `tools/remote-images.txt` and commits them.


There are no stock photos and no scraped images. Everything else is generated by [`tools/gen_images.py`](tools/gen_images.py) (Python + Pillow + NumPy): the dithered flowers, pixel bugs, kitty, shoggoth, dark forest, gallery pieces (Rule 30, a Mandelbrot crop, Voronoi, Gray–Scott, moiré, hash portraits), the catalogue schematics and the sepia "spirit photographs". To regenerate them:

```sh
python3 tools/gen_images.py
```

## Sources

The full bibliography is in [`shelf.html`](shelf.html). Research notes, with the facts and quotations the rooms rely on, are in [`docs/research.md`](docs/research.md). Quotations are short and attributed. Some of the authors quoted (Land's later work, Yarvin, parts of the Remilia scene) hold views this work treats critically. They are quoted to be looked at, not followed.

Made in 2026 by a human and a machine, talking. Inspired by, and with love for, mouchette.org.
