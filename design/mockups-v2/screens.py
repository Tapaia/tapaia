from build import page, sidebar, av, i, write, PEOPLE


def msg(key, text, time, badges='', mention=False, cont=False, extra=''):
    name, c = PEOPLE[key]
    if cont:
        return f'<div class="msg cont"><span class="spacer"></span><div class="content"><div class="text">{text}</div>{extra}</div></div>'
    cls = 'msg mention' if mention else 'msg'
    return f'''<div class="{cls}">{av(key, c)}<div class="content"><div class="meta"><span class="who">{name}</span>{badges}<span class="time">{time}</span></div>
      <div class="text">{text}</div>{extra}</div></div>'''


MEDAL = '<img class="px badge-ic" src="assets/icon-medal.png" alt="Founding Citizen" title="Founding Citizen">'
FLAME = '<img class="px badge-ic" src="assets/icon-flame.png" alt="On-chain arrival" title="On-chain arrival">'
SHIELD = '<img class="px badge-ic" src="assets/icon-shield.png" alt="Team" title="Verified team">'


def members(groups):
    out = ['<aside class="members">']
    for title, rows in groups:
        out.append(f'<div class="grp">{title}</div>')
        for key, status, badge, dot, *rest in rows:
            name, c = PEOPLE[key]
            away = ' away' if rest and rest[0] == 'away' else ''
            b = f'<img class="px b" src="assets/icon-{badge}.png" alt="">' if badge else ''
            out.append(f'<div class="mem{away}">{av(key, c, "s32", dot)}<div class="info"><div class="nm">{name}</div><div class="st">{status}</div></div>{b}</div>')
    out.append('</aside>')
    return ''.join(out)


SQUARE_MEMBERS = [
    ('FOUNDING CITIZENS — 3', [('ilse', 'just arrived', 'medal', ''), ('nessa', 'at the tea cart', 'medal', ''), ('corvin', 'idle', 'medal', 'idle')]),
    ('CITIZENS — 9', [('wren', 'herb swap at 6 lh', 'flame', ''), ('orla', 'by the maple', 'flame', ''), ('tobin', 'hood up', 'flame', ''),
                      ('pim', 'in the library', 'flame', ''), ('juniper', 'that’s you', 'flame', '')]),
    ('TEAM — 1', [('team', 'Tapaia team', 'shield', '')]),
    ('AWAY — 1', [('marek', 'back later', None, 'off', 'away')]),
]


def screen_square():
    feed = f'''
    <div class="feed">
      <div class="sysline"><img class="px" src="assets/icon-door.png" alt=""><b>Juniper Vale</b> has entered the square</div>
      {msg('corvin', 'Morning, all. The tea cart is open again, jasmine today ☕', '57656', MEDAL)}
      {msg('nessa', 'Save me a cup! Is the library still all business books?', '57699', MEDAL)}
      <div class="card-arrival"><div class="fig"><img class="px" src="assets/av-ilse.png" alt=""></div>
        <div><div class="k">{MEDAL} New arrival · Founding Citizen</div>
        <div class="q"><b>Ilse Hartwood</b> “Hello Tapaia! I brought cards and a terrible sense of direction.”</div></div>
        <div class="wave"><span class="btn-soft">👋 Wave hello</span><span class="time" style="font-size:12px;color:var(--text-3)">57761</span></div></div>
      <div class="replyline"><span class="bar"></span>{av('ilse','c1')}<b>Ilse Hartwood</b> Hello Tapaia! I brought cards…</div>
      {msg('tobin', 'Welcome, Ilse! Fair warning, the slide is cold this time of year.', '57784', FLAME,
           extra='<div class="reactions"><span class="react mine">👋 4</span><span class="react">🃏 2</span></div>')}
      <div class="card-speak"><div class="h"><img class="px" src="assets/icon-flame.png" alt="">Spoke to the Square · burned <span class="ph" style="text-transform:none">S</span> ZC
        <span class="v">{i('check','sm')}Verified on-chain {i('ext','sm')}</span></div>
        <div class="b">{av('wren','c2')}<div><div class="meta"><span class="who">Wren Halloway</span><span class="time">57801</span></div>
        <div class="text">Herb swap at the tea cart at 6 longhours. Bring cuttings, take cuttings 🌿</div></div></div></div>
      {msg('orla', '<span class="at">@Ilse Hartwood</span> come sit with us by the maple, there’s room on the bench.', '57832', FLAME, mention=True)}
      <div class="sysline"><img class="px" src="assets/icon-door.png" alt=""><b>Marek Stonebrook</b> left the square</div>
    </div>'''
    composer = f'''
    <div class="composer">
      <div class="row"><span class="iconbtn">{i('plus')}</span>
        <div class="input">On my way! Saving the bench by the maple<span class="caret"></span></div>
        <span class="iconbtn">{i('smile')}</span>
        <span class="seg"><span class="on">{i('chat','sm')}Say</span><span class="burn"><img class="px" src="assets/icon-flame.png" alt="">Speak</span></span>
        <span class="send">{i('send')}</span></div>
      <div class="foot">Say is free. <b style="color:var(--ember-600);font-weight:600">Speak</b> posts to the zipcoin Book: burns ≥ <span class="ph">S</span> ZC + gas, permanent and public.</div>
    </div>'''
    body = f'''<div class="app">{sidebar('square', unread={'announcements': 1, 'general': True, 'market': True})}
  <main class="main">
    <div class="topbar"><div class="title"><img class="px" src="assets/icon-tree.png" alt="">Tapaia Square</div>
      <div class="topic">Tea cart’s open. Say hello to new arrivals, and speak as your citizen.</div>
      <div class="acts"><span class="stack"><span class="avs">{av('ilse','c1')}{av('nessa','c5')}{av('wren','c2')}</span>14</span>
        <span class="iconbtn">{i('pin')}</span><span class="iconbtn">{i('bell')}</span><span class="iconbtn on">{i('users')}</span><span class="iconbtn">{i('search')}</span></div></div>
    <div class="banner"><div class="over"><span class="pill glass"><img class="px" src="assets/icon-tree.png" alt="">In character · Meldan</span>
      <h2>Tapaia Square</h2><p>Sit down, drink tea, the shops are nearby. Speak as your citizen.</p></div>
      <div class="clock"><span class="pixel">57847</span><span>ticks · 5 longhours</span></div></div>
    {feed}{composer}
  </main>
  {members(SQUARE_MEMBERS)}
</div>'''
    write('03-tapaia-square.html', page('Tapaia Square (desktop)', body, kind='desk'))


OOC = {'odessa': 'brightmoss', 'sorrel': 'sorrelf', 'lumi': 'lumi_a', 'bram': 'bram', 'juniper': 'jvale'}


def omsg(key, text, time, tag='', mention=False, extra=''):
    c = PEOPLE[key][1]
    cls = 'msg mention' if mention else 'msg'
    return f'''<div class="{cls}">{av(key, c)}<div class="content"><div class="meta"><span class="who">{OOC[key]}</span>{tag}<span class="time">{time}</span></div>
      <div class="text">{text}</div>{extra}</div></div>'''


def screen_general():
    feed = f'''
    <div class="feed">
      <div class="daysep">Today</div>
      {omsg('bram', 'Phase 1 beta notes are up in <span class="at">#dev-updates</span>. Big one: push notifications now work when you add Tapaia to your home screen on iPhone and Android.', '9:12 AM', '<span class="tagteam">TEAM</span>',
            extra='<div class="reactions"><span class="react mine">🎉 12</span><span class="react">🙌 5</span><span class="react">🍵 3</span></div><div class="thread">' + i('thread','sm') + '6 replies · last reply 4m ago</div>')}
      {omsg('odessa', 'Installed it on my phone and the first mention came through instantly. Honestly smoother than the old group chat 👋', '9:20 AM')}
      <div class="replyline"><span class="bar"></span>{av('odessa','c2')}<b>brightmoss</b> Installed it on my phone and the first mention came through…</div>
      {omsg('sorrel', 'Same here. Is there a way to schedule dark mode for after sunset?', '9:24 AM')}
      {omsg('lumi', 'Source is up if anyone wants to dig in, prompts and art generators included:', '9:31 AM',
            extra='<div class="linkcard"><span class="thumb"><img class="px" src="assets/icon-tea.png" alt=""></span><div><div class="u">github.com/tapaia/tapaia</div><div class="t">Tapaia: open-source community chat for $ZC</div><div class="d">GPL v3 · based on Snowmoon by Vitalik Buterin · not affiliated</div></div></div>')}
      <div class="sysline">👋 <b>sorrelf</b> just became a citizen. Say hi!</div>
      {omsg('odessa', '<span class="at">@jvale</span> did your arrival post confirm okay?', '9:38 AM', mention=True)}
      {omsg('juniper', 'Yep, about a minute. The preview made it really clear what I was burning before I signed.', '9:40 AM')}
    </div>
    <div class="typing"><span class="dots"><i></i><i></i><i></i></span><b style="font-weight:600;color:var(--text-2)">lumi_a</b> is typing…</div>'''
    composer = f'''
    <div class="composer"><div class="row"><span class="iconbtn">{i('plus')}</span>
      <div class="input"><span class="ph-text">Message #general</span></div>
      <span class="iconbtn">{i('image')}</span><span class="iconbtn">{i('smile')}</span><span class="send">{i('send')}</span></div></div>'''
    mem = ['<aside class="members">']
    groups = [('TEAM — 1', [('bram', 'shipping the beta', 'shield', '')]),
              ('MODERATORS — 2', [('odessa', 'here to help', None, ''), ('lumi', 'reading the repo', None, '')]),
              ('ONLINE — 125', [('sorrel', 'new citizen 🎉', None, ''), ('juniper', 'that’s you', None, ''), ('nessa', 'in Tapaia Square', None, ''), ('pim', '', None, 'idle'), ('corvin', '', None, 'idle')]),
              ('OFFLINE', [('marek', '', None, 'off', 'away')])]
    names = {'nessa': 'nessaq', 'pim': 'tallowpim', 'corvin': 'ashdale', 'marek': 'stonebrook'}
    for title, rows in groups:
        mem.append(f'<div class="grp">{title}</div>')
        for key, st, badge, dot, *rest in rows:
            c = PEOPLE[key][1]
            nm = OOC.get(key) or names.get(key, key)
            away = ' away' if rest else ''
            b = f'<img class="px b" src="assets/icon-{badge}.png" alt="">' if badge else ''
            stt = f'<div class="st">{st}</div>' if st else ''
            mem.append(f'<div class="mem{away}">{av(key, c, "s32", dot)}<div class="info"><div class="nm">{nm}</div>{stt}</div>{b}</div>')
    mem.append('</aside>')
    body = f'''<div class="app">{sidebar('general', unread={'announcements': 1, 'market': True, 'dev-updates': 3}, me=('juniper', 'jvale', 'Online'))}
  <main class="main">
    <div class="topbar"><div class="title"><span class="hash">#</span>general</div>
      <div class="topic">Everyday community talk. Price talk lives in #market.</div>
      <div class="acts"><span class="stack"><span class="avs">{av('odessa','c2')}{av('sorrel','c5')}{av('lumi','c6')}</span>128</span>
        <span class="iconbtn">{i('pin')}</span><span class="iconbtn">{i('bell')}</span><span class="iconbtn on">{i('users')}</span><span class="iconbtn">{i('search')}</span></div></div>
    <div class="pinbar">{i('pin','sm')}<span><b>Pinned:</b> the only real ZC is <code>0x4E67…8722</code>. Staff never DM first or ask for your seed phrase.</span><span class="r">{i('x','sm')}</span></div>
    {feed}{composer}
  </main>
  {''.join(mem)}
</div>'''
    write('04-general-dark.html', page('#general (desktop, dark theme)', body, theme='dark', kind='desk'))


SIGNIN_CSS = '''
.split { display: flex; height: 900px; }
.hero { position: relative; width: 800px; margin: 16px 0 16px 16px; border-radius: 28px; overflow: hidden;
  background: url('assets/scene-landing.png') -60px bottom / 1600px 1000px no-repeat; box-shadow: var(--shadow-md); }
.hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(35,20,47,0) 35%, rgba(35,20,47,.72) 85%); }
.hero .brand { position: absolute; z-index: 2; left: 24px; top: 22px; display: flex; align-items: center; gap: 10px; padding: 6px 14px 6px 6px; border-radius: 16px; background: rgba(255,255,255,.9); box-shadow: var(--shadow-sm); }
.hero .brand b { font-size: 17px; letter-spacing: -.01em; }
.hero .copy { position: absolute; z-index: 2; left: 32px; right: 32px; bottom: 32px; color: #fff; }
.hero h1 { margin: 0 0 8px; font-size: 40px; line-height: 1.08; letter-spacing: -.03em; font-weight: 750; text-shadow: 0 2px 12px rgba(0,0,0,.25); }
.hero p { margin: 0; font-size: 17px; opacity: .95; max-width: 520px; }
.hero .proof { display: flex; align-items: center; gap: 10px; margin-top: 18px; font-size: 14px; font-weight: 600; }
.hero .proof .avs { display: flex; } .hero .proof .av { margin-left: -8px; border: 2px solid rgba(255,255,255,.9); border-radius: 50%; width: 34px; height: 34px; }
.hero .proof .av:first-child { margin-left: 0; } .hero .proof .av img { width: 32px; height: 32px; margin-bottom: -6px; }
.form { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0 40px; }
.form .inner { width: 420px; }
.form h2 { margin: 0 0 6px; font-size: 30px; letter-spacing: -.03em; font-weight: 750; }
.form .lede { margin: 0 0 22px; color: var(--text-2); font-size: 15.5px; }
.wallets { display: flex; flex-direction: column; gap: 8px; }
.wrow { display: flex; align-items: center; gap: 14px; height: 58px; padding: 0 14px 0 10px; border-radius: 14px; background: var(--surface); border: 1px solid var(--line); box-shadow: var(--shadow-sm); font-weight: 600; font-size: 15.5px; }
.wrow .ico { width: 40px; height: 40px; border-radius: 11px; display: grid; place-items: center; background: var(--sidebar); }
.wrow .ico img { width: 24px; height: 24px; }
.wrow .r { margin-left: auto; display: flex; align-items: center; gap: 8px; color: var(--text-3); }
.wrow.hover { border-color: var(--robe-500); box-shadow: 0 0 0 4px var(--robe-100), var(--shadow-sm); }
.wrow .sub { font-weight: 500; font-size: 13px; color: var(--text-3); }
.siwe { display: flex; gap: 10px; align-items: flex-start; margin-top: 18px; padding: 12px 14px; border-radius: 14px; background: var(--leaf-50); border: 1px solid #cfe6c6; color: var(--leaf-700); font-size: 13.5px; }
.siwe svg { margin-top: 1px; }
.alt { margin-top: 18px; display: flex; justify-content: space-between; font-size: 14px; color: var(--text-2); }
.legal { margin-top: 28px; font-size: 12px; color: var(--text-3); line-height: 1.5; }
'''


def screen_signin():
    def wrow(key, name, right='', cls='', sub=''):
        s = f'<span class="sub">{sub}</span>' if sub else ''
        return f'<div class="wrow {cls}"><span class="ico"><img class="px" src="assets/wallet-{key}.png" alt=""></span><div>{name}<br>{s}</div><span class="r">{right}{i("chev-r","sm")}</span></div>' if sub else \
               f'<div class="wrow {cls}"><span class="ico"><img class="px" src="assets/wallet-{key}.png" alt=""></span>{name}<span class="r">{right}{i("chev-r","sm")}</span></div>'
    det = '<span class="pill ok">Detected</span>'
    body = f'''<div class="split">
  <section class="hero">
    <div class="brand"><span class="logo-tile"><img class="px" src="assets/icon-tea.png" alt=""></span><b>Tapaia</b></div>
    <div class="copy"><h1>The town square for<br>the $ZC community.</h1>
      <p>Chat like you would on Telegram. Step into Veridia and speak as your citizen whenever you feel like it.</p>
      <div class="proof"><span class="avs">{av('nessa','c5')}{av('wren','c2')}{av('tobin','c1')}{av('pim','c3')}</span>Open source · based on <i>Snowmoon</i></div></div>
  </section>
  <section class="form"><div class="inner">
    <h2>Welcome to Tapaia</h2>
    <p class="lede">Sign in with the wallet you already use.</p>
    <div class="wallets">
      {wrow('rabby', 'Rabby', det, 'hover')}
      {wrow('metamask', 'MetaMask', det)}
      {wrow('coinbase', 'Coinbase Wallet')}
      {wrow('rainbow', 'Rainbow')}
      {wrow('trust', 'Trust Wallet')}
      {wrow('walletconnect', 'WalletConnect', '<span class="pill neutral">' + i('qr','sm') + 'QR</span>', sub='Phone wallets and many more')}
    </div>
    <div class="siwe">{i('shield','sm')}<div><b>Free, no transaction, no gas.</b> You'll sign a one-time message (Sign-In with Ethereum) to prove the wallet is yours. We never touch your funds.</div></div>
    <div class="alt"><span>Just looking? <span class="link">Browse #lobby →</span></span><span class="link">Get help</span></div>
    <div class="legal">Based on <i>Snowmoon</i> by Vitalik Buterin, used under GPL v3. Not affiliated with Vitalik Buterin, zipcoin.cash or Stockereum. Staff never DM first and never ask for your seed phrase.</div>
  </div></section>
</div>'''
    write('01-sign-in.html', page('Sign in (desktop)', body, kind='desk', extra_css=SIGNIN_CSS))


ARRIVAL_CSS = '''
.dim { position: absolute; inset: 0; background: rgba(29, 20, 38, .45); backdrop-filter: blur(2px); z-index: 5; }
.modal { position: absolute; z-index: 6; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 1000px; height: 850px; border-radius: 24px;
  background: var(--surface); box-shadow: var(--shadow-lg); display: flex; flex-direction: column; overflow: hidden; }
.mh { display: flex; align-items: center; gap: 14px; padding: 22px 26px 18px; border-bottom: 1px solid var(--line); }
.mh .medal { width: 48px; height: 48px; border-radius: 14px; background: var(--gold-100); display: grid; place-items: center; }
.mh .medal img { width: 24px; height: 24px; }
.mh h2 { margin: 0; font-size: 22px; letter-spacing: -.02em; }
.mh p { margin: 2px 0 0; color: var(--text-2); font-size: 14.5px; }
.mh .x { margin-left: auto; }
.mb { flex: 1; display: flex; gap: 22px; padding: 18px 26px; min-height: 0; }
.mcol { display: flex; flex-direction: column; gap: 12px; }
.box { border: 1px solid var(--line); border-radius: 16px; padding: 16px; background: var(--surface); }
.box h4 { margin: 0 0 8px; font-size: 13px; color: var(--text-3); font-weight: 650; letter-spacing: .02em; }
.slots-big { font-size: 26px; font-weight: 750; letter-spacing: -.02em; margin: 2px 0 10px; }
.prog { height: 10px; border-radius: 99px; background: var(--sidebar-2); overflow: hidden; }
.prog i { display: block; height: 100%; width: 72%; border-radius: 99px; background: linear-gradient(90deg, var(--gold-500), #f2c84b); }
.small { font-size: 13px; color: var(--text-3); }
.kv { display: flex; justify-content: space-between; font-size: 14px; padding: 7px 0; border-top: 1px solid var(--line); }
.kv:first-of-type { border-top: 0; }
.notice-soft { display: flex; gap: 10px; padding: 12px; border-radius: 12px; background: var(--robe-50); color: var(--robe-700); font-size: 13.5px; }
.seg.big span { height: 36px; padding: 0 16px; font-size: 14px; }
.field label { display: block; font-size: 13px; font-weight: 650; color: var(--text-2); margin-bottom: 6px; }
.ta { min-height: 72px; padding: 12px 14px; border-radius: 12px; border: 1.5px solid var(--robe-500); box-shadow: 0 0 0 4px var(--robe-100); font-size: 16px; }
.fieldrow { display: flex; justify-content: space-between; margin-top: 6px; font-size: 12.5px; color: var(--text-3); }
.callout { border-radius: 16px; border: 1px solid #f0b98a; background: var(--ember-50); padding: 14px 16px; }
.callout .t { display: flex; align-items: center; gap: 8px; font-weight: 700; color: var(--ember-600); font-size: 15px; margin-bottom: 6px; }
.callout .t img { width: 18px; height: 18px; }
.callout ul { margin: 0; padding-left: 18px; font-size: 14px; color: var(--text); line-height: 1.55; }
.costs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 12px; }
.cost { background: var(--surface); border: 1px solid #f3d3b6; border-radius: 12px; padding: 8px 10px; }
.cost .k { font-size: 11.5px; color: var(--text-3); font-weight: 600; }
.cost .v { font-size: 15px; font-weight: 700; margin-top: 2px; display: flex; align-items: center; gap: 6px; }
.cost .v img { width: 16px; height: 16px; }
.chk { display: flex; align-items: center; gap: 10px; font-size: 14px; }
.chk .b { width: 20px; height: 20px; border-radius: 6px; border: 1.5px solid var(--line-2); display: grid; place-items: center; flex: none; }
.chk .b.on { background: var(--robe-600); border-color: var(--robe-600); color: #fff; }
.mf { display: flex; align-items: center; gap: 12px; padding: 16px 26px; border-top: 1px solid var(--line); background: var(--bg); }
.steps { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--text-3); font-weight: 600; }
.steps .s { width: 26px; height: 6px; border-radius: 99px; background: var(--line-2); }
.steps .s.on { background: var(--robe-600); } .steps .s.done { background: var(--leaf-600); }
.mf .r { margin-left: auto; display: flex; gap: 10px; }
.card-arrival.pv { margin: 0; }
'''


def screen_arrival():
    modal = f'''
  <div class="dim"></div>
  <div class="modal">
    <div class="mh"><span class="medal"><img class="px" src="assets/icon-medal.png" alt=""></span>
      <div><h2>Become a citizen of Tapaia</h2><p>Your arrival post is how you join. Everyone in Tapaia Square gets to greet you.</p></div>
      <span class="iconbtn x">{i('x')}</span></div>
    <div class="mb">
      <div class="mcol" style="width:330px">
        <div class="box"><h4>FOUNDING CITIZEN SLOTS</h4>
          <div class="slots-big"><span class="ph">X−n</span> of <span class="ph">X</span> left</div>
          <div class="prog"><i></i></div>
          <div class="small" style="margin-top:6px">Bar is illustrative. X isn't decided yet.</div>
          <div style="margin-top:12px">
            <div class="kv"><span>Founder window</span><b><span class="ph">dates TBD</span></b></div>
            <div class="kv"><span>Limit</span><b>1 per wallet</b></div>
            <div class="kv"><span>Eligibility</span><b><span class="ph">rule TBD</span></b></div></div>
        </div>
        <div class="notice-soft">{i('info','sm')}<div>This wallet isn't eligible for a free founder slot, so you'll join with an on-chain arrival post.</div></div>
        <div class="box"><h4>AS A CITIZEN YOU CAN</h4>
          <div style="font-size:14px;line-height:1.75">✓ Post in every community channel<br>✓ Chat as your citizen in Tapaia Square<br>✓ Build your pixel avatar<br><span class="small">One-time entry. Never re-checked.</span></div></div>
        <div class="notice-soft" style="background:var(--leaf-100);color:var(--leaf-700)">{i('shield','sm')}<div>After you sign, we check the burn on-chain. Once it's confirmed, you walk into Tapaia Square.</div></div>
      </div>
      <div class="mcol" style="flex:1">
        <span class="seg big" style="align-self:flex-start"><span><img class="px" src="assets/icon-medal.png" alt="">Founding Citizen · free</span><span class="burn on"><img class="px" src="assets/icon-flame.png" alt="">Arrival post · burn</span></span>
        <div class="field"><label>Your arrival message</label>
          <div class="ta">Hello Tapaia! Herb grower from Kalimar, here for the tea and the talk.<span class="caret"></span></div>
          <div class="fieldrow"><span>Posting as <b style="color:var(--text-2)">Wren Halloway</b> · keep it short and kind</span><span>73 / 280 bytes</span></div></div>
        <div class="card-arrival pv"><div class="fig"><img class="px" src="assets/av-wren.png" alt=""></div>
          <div><div class="k"><img class="px" src="assets/icon-flame.png" alt="" style="width:14px;height:14px">Preview · new citizen</div>
          <div class="q"><b>Wren Halloway</b> “Hello Tapaia! Herb grower from Kalimar, here for the tea and the talk.”</div></div></div>
        <div class="callout"><div class="t"><img class="px" src="assets/icon-flame.png" alt="">This burns real ZC and is permanent</div>
          <ul><li>Posted to the zipcoin Book forever: public, can't be edited or deleted, reposted to X by @zipcoinbook.</li>
            <li>Links this wallet to Tapaia publicly. Not refundable. We never hold your tokens or keys.</li>
            <li>Only real ZC counts: <b>0x4E67…8722</b></li></ul>
          <div class="costs">
            <div class="cost"><div class="k">BURN</div><div class="v"><img class="px" src="assets/icon-coin.png" alt=""><span class="ph">E</span> ZC</div></div>
            <div class="cost"><div class="k">≈ VALUE + GAS</div><div class="v">live estimate</div></div>
            <div class="cost"><div class="k">ZIPCOIN MINIMUM</div><div class="v">1,000 ZC</div></div></div></div>
        <div class="chk"><span class="b on">{i('check','sm')}</span>I understand this post is permanent and public.</div>
        <div class="chk"><span class="b"></span>I understand the burn can't be refunded.</div>
      </div>
    </div>
    <div class="mf"><div class="steps"><span class="s done"></span><span class="s on"></span><span class="s"></span><span class="s"></span>Step 2 of 4 · write your arrival</div>
      <div class="r"><span class="btn ghost">Back</span><span class="btn burn disabled"><img class="px" src="assets/icon-flame.png" alt="">Sign &amp; burn in wallet</span></div></div>
  </div>'''
    body = f'''<div class="app">{sidebar('lobby', unread={'announcements': 1}, me=('wren', 'Wren Halloway', 'Not a citizen yet'))}
  <main class="main"><div class="topbar"><div class="title"><span class="hash">#</span>lobby</div><div class="topic">Say hi and look around. Become a citizen to post everywhere.</div></div>
    <div class="feed">{omsg('bram','Welcome to Tapaia! Make your arrival post to join, or ask anything in #support.','9:02 AM','<span class="tagteam">TEAM</span>')}</div></main>
</div>{modal}'''
    write('02-arrival.html', page('Arrival (desktop)', body, kind='desk', extra_css=ARRIVAL_CSS))


MOBILE_CSS = """
.phone-page { display: flex; flex-direction: column; background: var(--bg); position: relative; }
.sb { height: 47px; flex: none; display: flex; align-items: center; justify-content: space-between; padding: 6px 28px 0 34px; font-size: 16px; font-weight: 650; letter-spacing: -.01em; }
.sb .r { display: flex; align-items: center; gap: 6px; }
.sig { display: flex; align-items: flex-end; gap: 2px; height: 12px; } .sig i { width: 3px; border-radius: 1px; background: var(--text); display: block; }
.wifi { width: 16px; height: 12px; }
.batt { width: 25px; height: 12px; border-radius: 4px; border: 1.5px solid rgba(31,26,36,.4); padding: 1.5px; position: relative; }
.batt i { display: block; height: 100%; width: 75%; background: var(--text); border-radius: 2px; }
.mtop { height: 56px; flex: none; display: flex; align-items: center; gap: 10px; padding: 0 10px 0 6px; border-bottom: 1px solid var(--line); background: var(--surface); }
.mtop .back { display: flex; align-items: center; color: var(--robe-600); font-weight: 600; font-size: 15px; gap: 0; }
.mtop .back .n { min-width: 20px; height: 20px; padding: 0 6px; border-radius: 99px; background: var(--robe-100); color: var(--robe-600); font-size: 12px; display: grid; place-items: center; font-weight: 700; }
.mtop .room { display: flex; align-items: center; gap: 10px; min-width: 0; flex: 1; }
.mtop .tile { width: 36px; height: 36px; border-radius: 11px; background: var(--leaf-100); display: grid; place-items: center; flex: none; }
.mtop .tile img { width: 24px; height: 24px; }
.mtop .nm { font-weight: 700; font-size: 16px; letter-spacing: -.01em; line-height: 1.2; }
.mtop .st { font-size: 12.5px; color: var(--text-3); display: flex; align-items: center; gap: 5px; }
.mtop .st .g { width: 7px; height: 7px; border-radius: 50%; background: var(--circle); }
.mbanner { position: relative; flex: none; margin: 10px 12px 2px; height: 84px; border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-sm);
  background: url('assets/scene-header.png') 38% bottom / 820px 96px no-repeat, #93c1e6; }
.mbanner::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(35,20,47,.6), rgba(35,20,47,0) 70%); }
.mbanner .over { position: absolute; z-index: 2; left: 12px; top: 10px; color: #fff; }
.mbanner .over b { display: block; font-size: 15px; font-weight: 700; margin-top: 7px; text-shadow: 0 1px 2px rgba(0,0,0,.3); }
.mbanner .over span.s { font-size: 12px; opacity: .92; }
.mbanner .clock { position: absolute; z-index: 2; right: 10px; top: 10px; height: 24px; padding: 0 9px; border-radius: 99px; display: flex; align-items: center; gap: 6px;
  background: rgba(10,14,39,.82); color: #7fbcff; font-size: 11px; font-weight: 600; }
.mbanner .clock .pixel { font-size: 8px; color: #cfe6ff; }
.mfeed { flex: 1; min-height: 0; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; padding-bottom: 4px; }
.mfeed > * { flex-shrink: 0; }
.mfeed .msg { padding: 5px 14px; gap: 10px; }
.mfeed .msg .av { width: 36px; height: 36px; border-radius: 11px; }
.mfeed .msg .who { font-size: 14.5px; }
.mfeed .msg .text { font-size: 15px; line-height: 1.4; }
.mfeed .sysline { padding: 6px 14px; font-size: 12.5px; }
.mfeed .card-arrival { margin: 6px 12px; padding: 12px; gap: 12px; align-items: flex-start; }
.mfeed .card-arrival .fig { width: 52px; height: 60px; }
.mfeed .card-arrival .fig img { width: 32px; height: auto; }
.mfeed .card-arrival .k { font-size: 11px; }
.mfeed .card-arrival .q { font-size: 14.5px; line-height: 1.4; }
.mfeed .card-arrival .acts { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.mfeed .card-arrival .btn-soft { height: 30px; font-size: 12.5px; }
.mfeed .card-speak { margin: 6px 12px; }
.mfeed .card-speak .h { padding: 8px 12px; font-size: 11px; }
.mfeed .card-speak .b { padding: 10px 12px; gap: 10px; }
.mfeed .card-speak .b .av { width: 36px; height: 36px; border-radius: 11px; }
.mfeed .card-speak .b .text { font-size: 15px; line-height: 1.4; }
.mcomp { flex: none; background: var(--surface); border-top: 1px solid var(--line); padding: 8px 10px 0; }
.mcomp .modes { display: flex; align-items: center; gap: 8px; padding: 0 2px 8px; }
.mcomp .modes .hint { font-size: 12px; color: var(--text-3); }
.mcomp .row { display: flex; align-items: center; gap: 8px; }
.mcomp .field { flex: 1; min-height: 42px; border-radius: 21px; background: var(--bg); border: 1px solid var(--line-2); display: flex; align-items: center; padding: 0 8px 0 14px; font-size: 15px; }
.mcomp .field .ic { margin-left: auto; padding-left: 6px; color: var(--text-3); display: flex; }
.mcomp .plus { width: 36px; height: 36px; border-radius: 50%; background: var(--sidebar); display: grid; place-items: center; color: var(--text-2); flex: none; }
.mcomp .send { width: 42px; height: 42px; border-radius: 50%; flex: none; }
.homebar { height: 34px; flex: none; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 8px; background: var(--surface); }
.homebar i { width: 134px; height: 5px; border-radius: 99px; background: var(--text); display: block; }
"""


def status_bar():
    return f"""<div class="sb"><span>9:53</span><span class="r"><span class="sig"><i style="height:4px"></i><i style="height:6px"></i><i style="height:9px"></i><i style="height:12px"></i></span>
  <svg class="wifi" viewBox="0 0 16 12"><path d="M8 11.5 5.6 9a3.4 3.4 0 0 1 4.8 0zM2.8 6.3a7.4 7.4 0 0 1 10.4 0l-1.4 1.4a5.4 5.4 0 0 0-7.6 0zM0 3.5a11.3 11.3 0 0 1 16 0l-1.4 1.4a9.3 9.3 0 0 0-13.2 0z" fill="currentColor"/></svg>
  <span class="batt"><i></i></span></span></div>"""


def screen_mobile_square():
    body = f"""{status_bar()}
<div class="mtop"><span class="back">{i('chev-l','lg')}<span class="n">3</span></span>
  <div class="room"><span class="tile"><img class="px" src="assets/icon-tree.png" alt=""></span>
    <div style="min-width:0"><div class="nm">Tapaia Square</div><div class="st"><span class="g"></span>14 here · in character</div></div></div>
  <span class="stack" style="border:0;padding:0"><span class="avs">{av('ilse','c1')}{av('nessa','c5')}{av('wren','c2')}</span></span>
  <span class="iconbtn">{i('more')}</span></div>
<div class="mbanner"><div class="over"><span class="pill glass" style="height:20px;font-size:11px;padding:0 8px"><img class="px" src="assets/icon-tree.png" alt="" style="width:12px;height:12px">Meldan</span>
  <b>Tea cart’s open</b><span class="s">Speak as your citizen</span></div>
  <div class="clock"><span class="pixel">57847</span>ticks</div></div>
<div class="mfeed">
  <div class="sysline"><img class="px" src="assets/icon-door.png" alt=""><b>Nessa Quill</b> has entered the square</div>
  {msg('nessa', 'Save me a cup! Is the library still all business books?', '57699', MEDAL)}
  <div class="card-arrival"><div class="fig"><img class="px" src="assets/av-ilse.png" alt=""></div>
    <div style="min-width:0"><div class="k">{MEDAL} Founding Citizen</div>
    <div class="q"><b>Ilse Hartwood</b> “Hello Tapaia! I brought cards and a terrible sense of direction.”</div>
    <div class="acts"><span class="btn-soft">👋 Wave hello</span><span class="react mine" style="height:30px">👋 6</span></div></div></div>
  {msg('tobin', 'Welcome, Ilse! Fair warning, the slide is cold this time of year.', '57784', FLAME)}
  <div class="card-speak"><div class="h"><img class="px" src="assets/icon-flame.png" alt="">Spoke · burned <span class="ph" style="text-transform:none">S</span> ZC
    <span class="v">{i('check','sm')}On-chain</span></div>
    <div class="b">{av('wren','c2')}<div><div class="meta"><span class="who">Wren Halloway</span><span class="time">57801</span></div>
    <div class="text">Herb swap at the tea cart at 6 longhours. Bring cuttings, take cuttings 🌿</div></div></div></div>
  <div class="sysline"><img class="px" src="assets/icon-door.png" alt=""><b>Juniper Vale</b> has entered the square</div>
</div>
<div class="mcomp">
  <div class="modes"><span class="seg"><span class="on">{i('chat','sm')}Say</span><span class="burn"><img class="px" src="assets/icon-flame.png" alt="">Speak</span></span><span class="hint">Say is free · Speak burns ZC</span></div>
  <div class="row"><span class="plus">{i('plus')}</span><div class="field" style="white-space:nowrap">Saving the bench by the maple<span class="caret"></span><span class="ic">{i('smile')}</span></div><span class="send">{i('send')}</span></div>
</div>
<div class="homebar"><i></i></div>"""
    write('05-mobile-square.html', page('Tapaia Square (mobile)', body, kind='phone-page', extra_css=MOBILE_CSS))


PROFILE_CSS = MOBILE_CSS + """
.ptop { height: 52px; flex: none; display: flex; align-items: center; padding: 0 8px; position: relative; }
.ptop .t { position: absolute; left: 0; right: 0; text-align: center; font-weight: 700; font-size: 16px; pointer-events: none; }
.ptop .back { color: var(--robe-600); display: flex; align-items: center; font-weight: 600; }
.ptop .r { margin-left: auto; }
.pscroll { flex: 1; min-height: 0; overflow: hidden; padding: 0 16px; display: flex; flex-direction: column; gap: 12px; }
.phero { position: relative; height: 176px; border-radius: 22px; overflow: hidden; flex: none;
  background: linear-gradient(180deg, #a9d1ee 0%, #d6ebf6 60%, transparent 60%), linear-gradient(rgba(255,255,255,.22), rgba(255,255,255,.22)), url('assets/tile-grass.png') 0 0 / 32px 32px; }
.phero::before { content: ''; position: absolute; left: 0; right: 0; top: 60%; height: 4px; background: rgba(36,69,42,.22); }
.phero .ava { position: absolute; left: 50%; bottom: 18px; transform: translateX(-50%); width: 80px; height: auto; }
.phero .shadow { position: absolute; left: 50%; bottom: 13px; transform: translateX(-50%); width: 72px; height: 12px; border-radius: 50%; background: rgba(20,40,20,.35); }
.phero .tl { position: absolute; left: 12px; top: 12px; }
.phero .tr { position: absolute; right: 12px; top: 12px; display: flex; align-items: center; gap: 6px; height: 24px; padding: 0 9px; border-radius: 99px; background: rgba(10,14,39,.78); color: #cfe6ff; font-size: 8px; }
.pname { text-align: center; flex: none; margin-top: 2px; }
.pname h1 { margin: 0; font-size: 22px; letter-spacing: -.02em; line-height: 1.2; }
.pname .h { font-size: 13.5px; color: var(--text-3); margin-top: 2px; }
.pname .chips { display: flex; justify-content: center; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); background: var(--surface); border: 1px solid var(--line); border-radius: 16px; flex: none; }
.stats > div { padding: 10px 8px; text-align: center; }
.stats > div + div { border-left: 1px solid var(--line); }
.stats .v { font-size: 17px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 5px; }
.stats .v img { width: 16px; height: 16px; }
.stats .k { font-size: 12px; color: var(--text-3); }
.stats .locked .v { color: var(--text-3); }
.sect { flex: none; }
.sect .sh { display: flex; align-items: baseline; justify-content: space-between; font-size: 13px; font-weight: 650; color: var(--text-2); margin: 2px 2px 8px; }
.sect .sh span { font-weight: 500; color: var(--text-3); font-size: 12px; }
.outfits { display: flex; gap: 8px; }
.of { width: 80px; flex: none; border-radius: 14px; background: var(--surface); border: 1.5px solid var(--line); padding: 8px 4px 6px; text-align: center; font-size: 11.5px; font-weight: 600; color: var(--text-2); line-height: 1.25; }
.of .im { height: 52px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 4px; }
.of img { width: 32px; height: auto; }
.of.sel { border-color: var(--robe-600); background: var(--robe-50); color: var(--robe-700); box-shadow: 0 0 0 3px var(--robe-100); }
.of.cut { width: 34px; overflow: hidden; border-right: 0; border-radius: 14px 0 0 14px; }
.swcard { background: var(--surface); border: 1px solid var(--line); border-radius: 16px; padding: 4px 14px; flex: none; }
.swrow { display: flex; align-items: center; height: 46px; gap: 10px; }
.swrow + .swrow { border-top: 1px solid var(--line); }
.swrow .lb { width: 62px; font-size: 14px; font-weight: 600; }
.swrow .sws { display: flex; gap: 9px; }
.sw { width: 26px; height: 26px; border-radius: 50%; box-shadow: inset 0 0 0 1px rgba(0,0,0,.12); position: relative; }
.sw.sel::after { content: ''; position: absolute; inset: -4px; border-radius: 50%; border: 2px solid var(--robe-600); }
.swrow .sub { font-size: 12px; color: var(--text-3); }
.tog { margin-left: auto; width: 44px; height: 26px; border-radius: 99px; background: var(--line-2); position: relative; flex: none; }
.tog::after { content: ''; position: absolute; left: 3px; top: 3px; width: 20px; height: 20px; border-radius: 50%; background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,.2); }
.savebar { flex: none; padding: 10px 16px 0; background: linear-gradient(180deg, rgba(250,247,242,0), var(--bg) 30%); }
.savebar .btn { width: 100%; height: 50px; border-radius: 14px; font-size: 16px; }
.phone-page .homebar { background: var(--bg); }
"""


def screen_mobile_profile():
    hair = [('#2e2630', 1), ('#7a4a2a', 0), ('#b5522b', 0), ('#d9a441', 0), ('#5a2f5e', 0), ('#9aa0ad', 0)]
    skin = [('#f6d7b8', 0), ('#e8b98c', 0), ('#c68a5a', 0), ('#8d5a3b', 1)]
    sw = lambda xs: ''.join(f'<span class="sw{" sel" if on else ""}" style="background:{c}"></span>' for c, on in xs)
    body = f"""{status_bar()}
<div class="ptop"><span class="back">{i('chev-l','lg')}Back</span><span class="t">Your citizen</span><span class="iconbtn r">{i('more')}</span></div>
<div class="pscroll">
  <div class="phero"><span class="pill glass tl"><img class="px" src="assets/icon-tree.png" alt="">Tapaia Square</span>
    <span class="tr pixel">57847</span>
    <span class="shadow"></span><img class="px ava" src="assets/av-juniper.png" alt="Avatar preview: purple slogan shirt, short black hair"></div>
  <div class="pname"><h1>Juniper Vale</h1><div class="h">Posts as <b style="color:var(--text-2)">@jvale</b> in community channels</div>
    <div class="chips"><span class="pill ember"><img class="px" src="assets/icon-flame.png" alt="">Citizen · arrival post</span>
      <span class="pill ok">{i('check','sm')}0x71C4…9A3f</span></div></div>
  <div class="stats"><div><div class="v">2</div><div class="k">Speaks</div></div>
    <div><div class="v">Day 3</div><div class="k">Arrived</div></div>
    <div class="locked"><div class="v">{i('lock','sm')}Rep</div><div class="k">Coming later</div></div></div>
  <div class="sect"><div class="sh">Outfit <span>From the Veridia wardrobe</span></div>
    <div class="outfits">
      <div class="of"><div class="im"><img class="px" src="assets/opt-j-robe.png" alt=""></div>Robe</div>
      <div class="of"><div class="im"><img class="px" src="assets/opt-j-hood.png" alt=""></div>Robe + hood</div>
      <div class="of"><div class="im"><img class="px" src="assets/opt-j-plain.png" alt=""></div>Plain shirt</div>
      <div class="of sel"><div class="im"><img class="px" src="assets/opt-j-slogan.png" alt=""></div>Slogan shirt</div>
    </div></div>
  <div class="swcard">
    <div class="swrow"><span class="lb">Hair</span><span class="sws">{sw(hair)}</span></div>
    <div class="swrow"><span class="lb">Skin</span><span class="sws">{sw(skin)}</span></div>
    <div class="swrow"><div><div style="font-size:14px;font-weight:600">Silk neck band</div><div class="sub">A silky cloth band, as in the book</div></div><span class="tog"></span></div>
  </div>
</div>
<div class="savebar"><span class="btn primary">Save citizen</span></div>
<div class="homebar"><i></i></div>"""
    write('06-mobile-profile.html', page('Profile and avatar (mobile)', body, kind='phone-page', extra_css=PROFILE_CSS))


def build():
    screen_signin()
    screen_arrival()
    screen_square()
    screen_general()
    screen_mobile_square()
    screen_mobile_profile()
