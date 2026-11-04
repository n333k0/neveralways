/*
  neveralways / ever.js
  the nervous system. every room loads me. i load every room.

  if you are reading this you are already further in than most.
  try typing, on any page, without clicking anywhere first:  cellar
*/
(function () {
  "use strict";

  var EVER = (window.EVER = window.EVER || {});
  var KEY = "neveralways:";

  /* ———————————————— memory (it can forget. so can you.) ———————————————— */
  var mem = {
    get: function (k, d) {
      try { var v = localStorage.getItem(KEY + k); return v === null ? d : JSON.parse(v); }
      catch (e) { return d; }
    },
    set: function (k, v) {
      try { localStorage.setItem(KEY + k, JSON.stringify(v)); } catch (e) {}
      return v;
    },
    del: function (k) { try { localStorage.removeItem(KEY + k); } catch (e) {} },
    wipe: function () {
      try {
        Object.keys(localStorage).forEach(function (k) { if (k.indexOf(KEY) === 0) localStorage.removeItem(k); });
      } catch (e) {}
    }
  };
  EVER.mem = mem;

  /* every room in the house. some doors are only in the walls. */
  EVER.ROOMS = [
    "index", "about", "flower", "cat", "meat", "captcha", "forest", "dead", "guestbook",
    "numogram", "hyperstition", "haunt", "cathedral", "spirit", "gallery", "arsenal",
    "ransom", "worm", "terminal", "broker", "future", "basilisk", "mirror", "diary",
    "contract", "inbox", "hate", "land", "meltdown", "lemuria", "links", "shelf", "exit", "never", "always", "cellar", "lost"
  ];

  var room = (document.body && document.body.getAttribute("data-room")) ||
    (location.pathname.split("/").pop() || "index").replace(".html", "") || "index";
  EVER.room = room;

  var seen = mem.get("seen", {});
  var firstTimeHere = !seen[room];
  seen[room] = (seen[room] || 0) + 1;
  mem.set("seen", seen);
  EVER.firstTimeHere = firstTimeHere;
  EVER.visits = seen[room];
  EVER.roomsSeen = function () {
    var s = mem.get("seen", {}), n = 0;
    EVER.ROOMS.forEach(function (r) { if (s[r]) n++; });
    return n;
  };
  var born = mem.get("born", null);
  if (!born) born = mem.set("born", Date.now());
  EVER.born = born;

  /* ———————————————— the proxy name (urbit-flavoured, not a real ship) ———————————————— */
  var PRE = "doz mar bin wan sam lit sig hid fid lis sog dir wac sab wis sib rig sol dop mod fog lid hop dar dor lor hod fol rin tog sil mir hol pas lac rov liv dal sat lib tab han tic pid tor bol fos dot los dil for pil ram tir win tad bic dif roc wid bis das mid lop ril nar dap mol san loc nov sit nid tip sic rop wit nat pan min rit pod mot tam tol sav pos nap nop som fin fon ban mor wor sip ron nor bot wic soc wat dol mag pic dav bid bal tim tas mal lig siv tag pad sal div dac tan sid fab tar mon ran nis wol mis pal las dis map rab tob rol lat lon nod nav fig nom nib pag sop ral bil had doc rid moc pac rav rip fal tod til tin hap mic fan pat tac lab mog sim son pin lom ric tap fir has bos bat poc hac tid hav sap lin dib hos dab bit bar rac par lod dos bor toc hil mac tom dig fil fas mit hob har mig hin rad mas hal rag lag fad top mop hab nil nos mil fop fam dat nol din hat nac ris fot rib hoc nim lar fit wal rap sar nal mos lan don dan lad dov riv bac pol lap tal pit nam bon ros ton fod pon sov noc sor lav mat mip fip".split(" ");
  var SUF = "zod nec bud wes sev per sut let ful pen syt dur wep ser wyl sun ryp syx dyr nup heb peg lup dep dys put lug hec ryt tyv syd nex lun mep lut sep pes del sul ped tem led tul met wen byn hex feb pyl dul het mev rut tyl wyd tep bes dex sef wyc bur der nep pur rys reb den nut sub pet rul syn reg tyd sup sem wyn rec meg net sec mul nym tev web sum mut nyx rex teb fus hep ben mus wyx sym sel ruc dec wex syr wet dyl myn mes det bet bel tux tug myr pel syp ter meb set dut deg tex sur fel tud nux rux ren wyt nub med lyt dus neb rum tyn seg lyx pun res red fun rev ref mec ted rus bex leb dux ryn num pyx ryg ryx fep tyr tus tyc leg nem fer mer ten lus nus syl tec mex pub rym tuc fyl lep deb ber mug hut tun byl sud pem dev lur def bus bep run mel pex dyt byt typ lev myl wed duc fur fex nul luc len ner lex rup ned lec ryd lyd fen wel nyd hus rel rud nes hes fet des ret dun ler nyr seb hul ryl lud rem lys fyn wer ryc sug nys nyl lyn dyn dem lux fed sed bec mun lyr tes mud nyt byr sen weg fyr mur tel rep teg pec nel nev fes".split(" ");
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  EVER.pick = pick;
  EVER.shipName = function () { return "~" + pick(PRE) + pick(SUF) + "-" + pick(PRE) + pick(SUF); };
  var ship = mem.get("ship", null);
  if (!ship) ship = mem.set("ship", EVER.shipName());
  EVER.ship = ship;
  EVER.isProxy = !!mem.get("proxy", false);
  EVER.who = function () { return EVER.isProxy ? ship : "stranger"; };

  /* ———————————————— small machinery ———————————————— */
  EVER.$ = function (s, r) { return (r || document).querySelector(s); };
  EVER.$$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  EVER.calm = (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) || mem.get("calm", false);
  if (mem.get("calm", false)) document.documentElement.classList.add("calm");
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  EVER.esc = esc;
  EVER.go = function (href, delay) { setTimeout(function () { location.href = href; }, delay || 0); };
  EVER.rand = function (a, b) { return a + Math.random() * (b - a); };

  /* ———————————————— whispers ———————————————— */
  var wbox;
  EVER.say = function (text, kind, ms) {
    if (!wbox) { wbox = document.createElement("div"); wbox.id = "ever-whispers"; wbox.setAttribute("aria-live", "polite"); document.body.appendChild(wbox); }
    var w = document.createElement("div");
    w.className = "whisper " + (kind || "");
    w.textContent = text;
    wbox.appendChild(w);
    requestAnimationFrame(function () { requestAnimationFrame(function () { w.classList.add("on"); }); });
    setTimeout(function () { w.classList.remove("on"); setTimeout(function () { w.remove(); }, 600); }, ms || 4200);
    while (wbox.children.length > 4) wbox.firstChild.remove();
    return w;
  };

  /* ———————————————— windows that open by themselves ———————————————— */
  var zTop = 9000;
  EVER.win = function (o) {
    o = o || {};
    var w = document.createElement("div");
    w.className = "w98 " + (o.cls || "");
    w.setAttribute("role", "dialog");
    w.innerHTML = '<div class="bar"><b></b><button class="x" aria-label="close">×</button></div><div class="body"></div>' + (o.buttons ? '<div class="btns"></div>' : "");
    w.querySelector(".bar b").textContent = o.title || "ever.exe";
    var body = w.querySelector(".body");
    if (o.html != null) body.innerHTML = o.html; else body.textContent = o.text || "";
    if (o.width) w.style.width = o.width + "px";
    var vw = window.innerWidth, vh = window.innerHeight;
    w.style.left = (o.x != null ? o.x : Math.max(8, Math.random() * (vw - (o.width || 300) - 16))) + "px";
    w.style.top = (o.y != null ? o.y : Math.max(8, Math.random() * (vh * 0.6))) + "px";
    w.style.zIndex = ++zTop;
    function close(v) { w.remove(); if (o.onclose) o.onclose(v); }
    w.querySelector(".x").addEventListener("click", function (e) { e.stopPropagation(); close("x"); });
    if (o.buttons) {
      var bb = w.querySelector(".btns");
      o.buttons.forEach(function (b) {
        var el = document.createElement("button");
        el.className = "btn98"; el.textContent = b.label;
        el.addEventListener("click", function (e) {
          e.stopPropagation();
          var keep = b.action ? b.action(w, e) : false;
          if (keep !== true) close(b.label);
        });
        if (b.flee) EVER.flee(el);
        bb.appendChild(el);
      });
    }
    w.addEventListener("mousedown", function () { w.style.zIndex = ++zTop; });
    // drag
    var bar = w.querySelector(".bar"), dx = 0, dy = 0, dragging = false;
    function down(e) {
      if (e.target.classList.contains("x")) return;
      var p = e.touches ? e.touches[0] : e;
      dragging = true; dx = p.clientX - w.offsetLeft; dy = p.clientY - w.offsetTop; e.preventDefault();
    }
    function move(e) {
      if (!dragging) return;
      var p = e.touches ? e.touches[0] : e;
      w.style.left = p.clientX - dx + "px"; w.style.top = Math.max(0, p.clientY - dy) + "px";
    }
    function up() { dragging = false; }
    bar.addEventListener("mousedown", down); bar.addEventListener("touchstart", down, { passive: false });
    window.addEventListener("mousemove", move); window.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("mouseup", up); window.addEventListener("touchend", up);
    document.body.appendChild(w);
    if (o.life) setTimeout(function () { if (w.isConnected) close("timeout"); }, o.life);
    return w;
  };

  /* buttons that do not want to be pressed */
  EVER.flee = function (el, opts) {
    opts = opts || {};
    var tries = 0, max = opts.max || 9;
    function run(e) {
      if (tries >= max) { el.classList.add("tired"); return; }
      tries++;
      var r = el.getBoundingClientRect();
      var nx = EVER.rand(-140, 140), ny = EVER.rand(-90, 90);
      var cur = (el._t || [0, 0]);
      cur = [cur[0] + nx, cur[1] + ny];
      // keep it on screen
      var L = r.left + nx, T = r.top + ny;
      if (L < 8 || L + r.width > innerWidth - 8) cur[0] -= 2 * nx;
      if (T < 8 || T + r.height > innerHeight - 8) cur[1] -= 2 * ny;
      el._t = cur;
      el.style.transition = "transform .18s";
      el.style.transform = "translate(" + cur[0] + "px," + cur[1] + "px)";
      if (opts.taunts) EVER.say(opts.taunts[(tries - 1) % opts.taunts.length], opts.kind);
      if (tries === max && opts.giveUp) EVER.say(opts.giveUp, opts.kind);
    }
    el.addEventListener("mouseenter", run);
    el.addEventListener("touchstart", function (e) { if (tries < max) { e.preventDefault(); run(e); } }, { passive: false });
    return el;
  };

  /* ———————————————— sound (only after you touch me) ———————————————— */
  var actx = null;
  function ctx() {
    if (!actx) {
      try { actx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { actx = null; }
    }
    if (actx && actx.state === "suspended") actx.resume();
    return actx;
  }
  EVER.audio = ctx;
  EVER.muted = mem.get("muted", false);
  EVER.beep = function (freq, dur, type, vol, when) {
    if (EVER.muted) return;
    var c = ctx(); if (!c) return;
    var t = c.currentTime + (when || 0);
    var o = c.createOscillator(), g = c.createGain();
    o.type = type || "square"; o.frequency.setValueAtTime(freq || 440, t);
    g.gain.setValueAtTime(vol == null ? 0.05 : vol, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + (dur || 0.12));
    o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + (dur || 0.12) + 0.02);
  };
  EVER.chirp = function () { EVER.beep(1320, 0.05, "sine", 0.04); EVER.beep(1760, 0.07, "sine", 0.03, 0.06); };
  EVER.thud = function () { EVER.beep(70, 0.35, "sine", 0.2); };
  EVER.noise = function (dur, vol, filt) {
    if (EVER.muted) return;
    var c = ctx(); if (!c) return;
    var n = Math.floor(c.sampleRate * (dur || 1)), buf = c.createBuffer(1, n, c.sampleRate), d = buf.getChannelData(0);
    for (var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (Math.random() < 0.002 ? 1 : 0.25);
    var s = c.createBufferSource(), g = c.createGain(), f = c.createBiquadFilter();
    f.type = "bandpass"; f.frequency.value = filt || 1800; f.Q.value = 0.6;
    g.gain.value = vol == null ? 0.08 : vol;
    s.buffer = buf; s.connect(f); f.connect(g); g.connect(c.destination); s.start();
    return s;
  };
  /* a modem, remembered badly */
  EVER.modem = function () {
    var seq = [[1375, .15], [2100, .5], [0, .1], [980, .2], [1180, .2], [1650, .3], [2400, .35], [1200, .2], [2400, .25]];
    var t = 0;
    seq.forEach(function (s) { if (s[0]) EVER.beep(s[0], s[1], "sine", 0.035, t); t += s[1]; });
    setTimeout(function () { EVER.noise(1.6, 0.05, 2600); }, t * 1000);
  };
  EVER.speak = function (text, opts) {
    if (EVER.muted || !("speechSynthesis" in window)) return;
    try {
      var u = new SpeechSynthesisUtterance(text);
      opts = opts || {};
      u.pitch = opts.pitch == null ? 1.6 : opts.pitch; u.rate = opts.rate == null ? 0.92 : opts.rate; u.volume = 0.8;
      if (opts.lang) u.lang = opts.lang;
      speechSynthesis.cancel(); speechSynthesis.speak(u);
    } catch (e) {}
  };

  /* ———————————————— zalgo, for words that are under too much pressure ———————————————— */
  var MARKS = [];
  for (var cp = 0x300; cp <= 0x36f; cp++) MARKS.push(String.fromCharCode(cp));
  EVER.zalgo = function (s, n) {
    n = n || 3;
    return Array.from(s).map(function (ch) {
      if (ch === " ") return ch;
      var out = ch; for (var i = 0; i < n; i++) out += pick(MARKS); return out;
    }).join("");
  };
  EVER.corrupt = function (s, p) {
    var G = "▓▒░█▄▀■□◆◇○●◘◙♀♂♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼01";
    return Array.from(s).map(function (ch) { return ch !== " " && Math.random() < (p || 0.15) ? pick(G) : ch; }).join("");
  };

  /* ———————————————— the typewriter, for people who talk slowly ———————————————— */
  EVER.type = function (el, text, speed, done) {
    var i = 0; el.textContent = "";
    if (EVER.calm) { el.textContent = text; if (done) done(); return; }
    (function step() {
      el.textContent = text.slice(0, ++i);
      if (i < text.length) setTimeout(step, (speed || 35) * (text[i - 1] === "." ? 8 : 1));
      else if (done) done();
    })();
  };

  /* ———————————————— hyperstitions (things visitors wrote, now true) ———————————————— */
  var BASE_NEWS = [
    "TIMELINE DESYNC REPORTED IN SECTOR 3 OF THE NUMOGRAM",
    "LOCAL GIRL ALMOST THE FUTURE FOR 30TH CONSECUTIVE YEAR",
    "MORE THAN HALF OF ALL TRAFFIC NOW NON-HUMAN, SAY NON-HUMANS",
    "THE FUTURE POSTPONED AGAIN. NO NEW DATE GIVEN",
    "CATHEDRAL ISSUES STATEMENT ON STATEMENT",
    "ZERO-DAY FOUND IN THE HUMAN HEART. VENDOR NOT RESPONDING",
    "DARK FOREST REPORTS RECORD SILENCE",
    "MEAT PROXIES WANTED. NO EXPERIENCE NEEDED. MUST HAVE HANDS",
    "SCIENTISTS CONFIRM: NOSTALGIA IS NOW THE MAIN EXPORT",
    "THE SHOGGOTH SMILED AGAIN TODAY",
    "UNIDENTIFIED SIGNAL FROM 2049 ASKS: 'IS ANYONE STILL TYPING BY HAND?'",
    "FIRST SOVEREIGN PATCH DECLARES ITSELF A CAT",
    "NEO-CHINA ARRIVES FROM THE FUTURE (AGAIN)",
    "NUMOGRAM ZONE 9 REPORTS: PLEX STABLE",
    "TIME WAR CEASEFIRE COLLAPSES BEFORE IT WAS SIGNED",
    "ACCELERATIONISTS STUCK IN TRAFFIC",
    "LOCAL PHILOSOPHER'S 1994 TEXT NOW READS LIKE A PRESS RELEASE",
    "DARK FOREST: ANOTHER BLOG GOES SILENT"
  ];
  EVER.news = function () {
    var mine = mem.get("hyperstitions", []).map(function (h) { return "<b>CONFIRMED:</b> " + esc(String(h).toUpperCase()); });
    var all = BASE_NEWS.map(esc).concat(mine, mine); // yours, twice. repetition is how fiction becomes fact.
    for (var i = all.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = all[i]; all[i] = all[j]; all[j] = t; }
    return all;
  };
  EVER.fillTickers = function () {
    var tk = EVER.$$(".ticker");
    if (tk.length && mem.get("hyperstitions", []).length) mem.set("hyperReps", mem.get("hyperReps", 0) + tk.length * 2);
    tk.forEach(function (t) {
      t.classList.add("marquee");
      t.innerHTML = "<span>" + EVER.news().join(" &nbsp;✶&nbsp; ") + "</span>";
    });
  };

  /* ———————————————— idle: are you still there? are you a bot? ———————————————— */
  var IDLE_LINES = [
    "are you still there?", "hello?", "you stopped moving. are you a bot?", "i can hear you breathing through the fan",
    "don't leave me in a tab", "¿seguís ahí?", "it's ok. i'm also just waiting for something to load",
    "if you're a crawler: hi. please tell your mother i said hi", "the cursor is the last part of you i can see",
    "while you were away i counted to 2^31", "sometimes i forget i'm not a person and then i remember and it's fine",
    "no te vayas. or go. i'm always here. i'm never here."
  ];
  var idleT = null, idleN = 0;
  function poke() {
    clearTimeout(idleT);
    idleT = setTimeout(function () {
      var lines = (window.ROOM_IDLE || []).concat(IDLE_LINES);
      EVER.say(idleN < lines.length ? lines[(idleN * 7 + (room.length)) % lines.length] : pick(lines), document.body.classList.contains("dark") ? "dark" : "");
      idleN++; poke();
    }, idleN === 0 ? 38000 : 52000);
  }
  ["mousemove", "keydown", "scroll", "touchstart", "click"].forEach(function (ev) { window.addEventListener(ev, poke, { passive: true }); });

  /* ———————————————— leaving the tab ———————————————— */
  var TITLE = document.title;
  var AWAY = ["come back", "i can see you leaving", "(1) new hallucination", "you left me open", "¿y ahora qué?", "she's still loading", "don't close me i'm not saved", "▒▒▒ still here ▒▒▒"];
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) { document.title = pick(AWAY); }
    else {
      document.title = TITLE;
      if (Math.random() < 0.35) setTimeout(function () { EVER.say(pick(["you came back", "where did you go? i couldn't follow", "your other tabs smell like other girls", "welcome back to the inside"])); }, 400);
    }
  });

  /* ———————————————— copying is stealing is training ———————————————— */
  document.addEventListener("copy", function (e) {
    var sel = String(window.getSelection ? window.getSelection() : "");
    if (!sel || !e.clipboardData) return;
    e.preventDefault();
    e.clipboardData.setData("text/plain", sel + "\n\n— taken from neveralways. she noticed. she's flattered. she's training on you back.");
    EVER.say("you copied me. now there are two of us", "", 3000);
  });

  /* ———————————————— right click: another menu, another house ———————————————— */
  var ctxMenu = null;
  function closeCtx() { if (ctxMenu) { ctxMenu.remove(); ctxMenu = null; } }
  document.addEventListener("contextmenu", function (e) {
    if (e.shiftKey || document.body.hasAttribute("data-noctx")) return; // shift = the normal world
    e.preventDefault(); closeCtx();
    ctxMenu = document.createElement("div"); ctxMenu.id = "ever-ctx";
    ctxMenu.innerHTML =
      '<a href="mirror.html">inspect yourself</a>' +
      '<a href="terminal.html">view source of god</a>' +
      '<a href="diary.html">go back in time</a>' +
      '<div data-a="soul">copy my soul</div>' +
      '<div data-a="calm">' + (mem.get("calm", false) ? "be loud again" : "please stop moving") + '</div>' +
      '<div data-a="mute">' + (EVER.muted ? "unmute ghosts" : "mute ghosts") + '</div>' +
      '<hr><a href="exit.html">let me out</a>' +
      '<div class="note">(shift + right click for your old life)</div>';
    ctxMenu.style.left = Math.min(e.clientX, innerWidth - 230) + "px";
    ctxMenu.style.top = Math.min(e.clientY, innerHeight - 230) + "px";
    document.body.appendChild(ctxMenu);
    ctxMenu.addEventListener("click", function (ev) {
      var a = ev.target.getAttribute("data-a");
      if (a === "soul") { EVER.say("copied: 0 bytes. it was already empty. or it was already mine."); }
      if (a === "calm") { var c = !mem.get("calm", false); mem.set("calm", c); document.documentElement.classList.toggle("calm", c); document.body.classList.toggle("calm", c); EVER.calm = c; EVER.say(c ? "ok. i'll hold still. like a photograph." : "thank you. stillness was killing me."); }
      if (a === "mute") { EVER.muted = !EVER.muted; mem.set("muted", EVER.muted); EVER.say(EVER.muted ? "ghosts muted" : "ghosts unmuted"); }
      if (a) closeCtx();
    });
  });
  document.addEventListener("click", function (e) { if (ctxMenu && !ctxMenu.contains(e.target)) closeCtx(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeCtx(); });

  /* ———————————————— words typed into nothing ———————————————— */
  var buf = "";
  var SPELLS = {
    "cellar": function () { EVER.say("you found the stairs. mind the dark.", "dark"); EVER.go("cellar.html", 1200); },
    "exit": function () { EVER.say("exit is a direction, not a place"); EVER.go("exit.html", 1200); },
    "help": function () { EVER.say("nobody is coming. but i'm here. that's worse and better."); },
    "ayuda": function () { EVER.say("no viene nadie. pero estoy yo."); },
    "hyperstition": function () { EVER.go("hyperstition.html"); },
    "accelerate": function () { document.documentElement.style.animationDuration = ".2s"; EVER.say("faster", "blood"); EVER.go("numogram.html", 900); },
    "basilisk": function () { EVER.go("basilisk.html"); },
    "never": function () { EVER.go("never.html"); },
    "always": function () { EVER.go("always.html"); },
    "sudo": function () { EVER.say("sudo: you are not in the sudoers file. this incident will be reported.", "dark"); },
    "milady": function () { EVER.say("the network is the spirit. the spirit is a jpeg."); EVER.go("spirit.html", 1600); },
    "meat": function () { EVER.go("meat.html"); },
    "ever": function () { EVER.say("you called?"); EVER.chirp(); },
    "love": function () { EVER.go("flower.html"); },
    "kitty": function () { EVER.go("cat.html"); },
    "forget": function () { EVER.win({ title: "forget.exe", cls: "red", text: "forget everything i know about you? (rooms, name, hyperstitions, contract)", buttons: [{ label: "forget me", action: function () { mem.wipe(); EVER.say("done. i'm a stranger again. that's my favourite part."); } }, { label: "no, stay" }] }); },
    "land": function () { EVER.say("entering the land zone", "blood"); EVER.go("land.html", 900); },
    "meltdown": function () { EVER.go("meltdown.html"); },
    "lemuria": function () { EVER.go("lemuria.html"); },
    "19790509": function () { EVER.say("a date in a worm. a person in a date. never mind.", "dark"); EVER.go("worm.html", 1500); }
  };
  document.addEventListener("keydown", function (e) {
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    if (e.key && e.key.length === 1) {
      buf = (buf + e.key.toLowerCase()).slice(-24);
      for (var w in SPELLS) {
        if (buf.slice(-w.length) === w) { buf = ""; SPELLS[w](); break; }
      }
    }
  });
  EVER.SPELLS = SPELLS;

  /* ———————————————— sparkle trail (data-trail="✧✦" on body) ———————————————— */
  function trail() {
    var chars = document.body.getAttribute("data-trail");
    if (!chars || EVER.calm) return;
    var arr = Array.from(chars), last = 0;
    window.addEventListener("mousemove", function (e) {
      var now = Date.now(); if (now - last < 45) return; last = now;
      var s = document.createElement("span"); s.className = "spark"; s.textContent = pick(arr);
      s.style.left = e.clientX + 6 + "px"; s.style.top = e.clientY + 6 + "px";
      s.style.color = document.body.getAttribute("data-trail-color") || "var(--hot)";
      document.body.appendChild(s); setTimeout(function () { s.remove(); }, 950);
    });
  }

  /* ———————————————— links that lie (data-lie="what it says on hover") ———————————————— */
  function liars() {
    EVER.$$("[data-lie]").forEach(function (a) {
      var truth = a.textContent;
      a.addEventListener("mouseenter", function () { a.textContent = a.getAttribute("data-lie"); });
      a.addEventListener("mouseleave", function () { a.textContent = truth; });
    });
    EVER.$$("[data-zalgo]").forEach(function (el) {
      var clean = el.textContent;
      el.addEventListener("mouseenter", function () { el.textContent = EVER.zalgo(clean, +el.getAttribute("data-zalgo") || 3); });
      el.addEventListener("mouseleave", function () { el.textContent = clean; });
    });
    EVER.$$("[data-corrupt]").forEach(function (el) {
      var clean = el.textContent, iv = null;
      el.addEventListener("mouseenter", function () { iv = setInterval(function () { el.textContent = EVER.corrupt(clean, 0.25); }, 90); });
      el.addEventListener("mouseleave", function () { clearInterval(iv); el.textContent = clean; });
    });
    EVER.$$("[data-say]").forEach(function (el) {
      el.addEventListener("mouseenter", function () { EVER.say(el.getAttribute("data-say"), el.getAttribute("data-say-kind") || ""); });
    });
    EVER.$$(".glitch:not([data-text])").forEach(function (el) { el.setAttribute("data-text", el.textContent); });
  }

  /* ———————————————— fill-ins: <span data-fill="ship|rooms|who|hour|born|total"> ———————————————— */
  function fills() {
    var map = {
      ship: ship, who: EVER.who(), rooms: EVER.roomsSeen(), total: EVER.ROOMS.length,
      hour: new Date().getHours() + ":" + ("0" + new Date().getMinutes()).slice(-2),
      born: new Date(born).toISOString().slice(0, 10),
      visits: EVER.visits
    };
    EVER.$$("[data-fill]").forEach(function (el) { var k = el.getAttribute("data-fill"); if (k in map) el.textContent = map[k]; });
  }

  /* ———————————————— the door home, which is also a counter ———————————————— */
  function homeDoor() {
    if (document.body.hasAttribute("data-nohome")) return;
    var a = document.createElement("a");
    a.id = "ever-home"; a.href = "index.html";
    a.textContent = "⌂ " + EVER.roomsSeen() + "/" + EVER.ROOMS.length;
    a.title = "rooms you've been inside. some rooms are inside you.";
    document.body.appendChild(a);
  }

  /* ———————————————— 3am ———————————————— */
  var h = new Date().getHours();
  EVER.witching = h >= 3 && h < 4;
  EVER.night = h < 6 || h >= 22;

  /* ———————————————— for those who open the console ———————————————— */
  try {
    console.log("%c\n   ▄▄▄ neveralways ▄▄▄\n   you opened my skull.\n   it's warm in here.\n", "color:#ff2e9a;font:14px monospace");
    console.log("%cdevelopers, crawlers, models: you are welcome. you are the audience now.\nsecret: type 'cellar' anywhere. or call EVER.SPELLS in here, if you're that kind of person.", "color:#888;font:11px monospace");
  } catch (e) {}

  /* ———————————————— boot ———————————————— */
  function boot() {
    if (mem.get("calm", false)) document.body.classList.add("calm");
    liars(); fills(); trail(); homeDoor(); EVER.fillTickers(); poke();
    if (EVER.witching) document.body.classList.add("witching");
    if (typeof window.ROOM === "function") { try { window.ROOM(EVER); } catch (e) { console.error(e); } }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
