import { I, Px, Av, BADGE_ICON } from '../ui';
import { nameIn, useS } from '../store';
import { canRead } from '../../shared/perms';
import type { PublicUser } from '../../shared/types';
import { openCard } from './Main';

export function Members() {
  const ch = useS((s) => s.channels.find((c) => c.id === s.active));
  const users = useS((s) => s.users);
  const me = useS((s) => s.me);
  if (!ch) return null;
  const all = Object.values(users).filter((u) => (ch.layer === 'dm' ? ch.members?.includes(u.id) : u.kind === 'bot' ? ch.id === 'feeds' : canRead(u, ch)));
  const on = (u: PublicUser) => u.presence !== 'off';
  let groups: [string, PublicUser[]][];
  if (ch.layer === 'ic') {
    const here = all.filter((u) => u.isCitizen && on(u) && u.room === 'square');
    const team = here.filter((u) => u.badges.includes('team'));
    const founders = here.filter((u) => !team.includes(u) && u.entry === 'founder');
    const cits = here.filter((u) => !team.includes(u) && !founders.includes(u));
    const away = all.filter((u) => u.isCitizen && u.kind !== 'bot' && !here.includes(u)).sort((a, b) => Number(on(b)) - Number(on(a))).slice(0, 8);
    groups = [['FOUNDING CITIZENS', founders], ['CITIZENS', cits], ['TEAM', team], ['ELSEWHERE', away]];
  } else if (ch.layer === 'dm') {
    groups = [['IN THIS CONVERSATION', all]];
  } else {
    const people = all.filter((u) => u.kind !== 'bot');
    const team = people.filter((u) => u.badges.includes('team'));
    const mods = people.filter((u) => !team.includes(u) && u.badges.includes('mod'));
    const rest = people.filter((u) => !team.includes(u) && !mods.includes(u));
    groups = [['TEAM', team], ['MODERATORS', mods], ['ONLINE', rest.filter(on)], ['BOTS', ch.id === 'feeds' ? all.filter((u) => u.kind === 'bot') : []], ['OFFLINE', rest.filter((u) => !on(u)).slice(0, 12)]];
  }
  const badge = (u: PublicUser) => {
    const b = ch.layer === 'ic' ? (u.badges.includes('team') ? 'team' : u.entry === 'founder' ? 'founder' : u.badges.includes('onchain') ? 'onchain' : null) : u.badges.includes('team') ? 'team' : u.badges.includes('bot') ? 'bot' : null;
    return b ? <Px src={BADGE_ICON[b]} className="b" /> : null;
  };
  return <>
    <div className="dim members-dim" onClick={() => useS.setState({ showMembers: false })} />
    <aside className="members" data-testid="members">
      <button className="iconbtn x" onClick={() => useS.setState({ showMembers: false })} aria-label="Close members"><I n="x" /></button>
      {groups.filter(([, xs]) => xs.length).map(([title, xs]) => <div key={title}>
        <div className="grp">{title} — {xs.length}</div>
        {xs.map((u) => <button key={u.id} className={`mem ${on(u) ? '' : 'away'}`} onClick={(e) => openCard(u.id, e)}>
          <Av u={u} size="s32" dot />
          <div className="info"><div className="nm">{nameIn(u, ch)}</div><div className="st">{u.id === me?.id ? 'that’s you' : u.status}</div></div>{badge(u)}
        </button>)}
      </div>)}
    </aside>
  </>;
}
