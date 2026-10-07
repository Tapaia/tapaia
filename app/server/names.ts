// Original, made-up names for demo and new wallet citizens.
const FIRST = ['Fennel', 'Hazel', 'Rowan', 'Tamsin', 'Ellery', 'Basil', 'Clover', 'Linden', 'Marlo', 'Quince', 'Saffi', 'Tarn', 'Wynn', 'Alder', 'Briar', 'Cass', 'Dov', 'Elsie', 'Ferris', 'Greer', 'Isla', 'Kit', 'Merrin', 'Nell'];
const LAST = ['Ashby', 'Fairbank', 'Hollins', 'Kettle', 'Larch', 'Meadows', 'Pennant', 'Rookwood', 'Sallow', 'Tumble', 'Underhill', 'Wexford', 'Yarrow', 'Bellweather', 'Copperfield', 'Dunmore', 'Greenhill', 'Marsh'];
const pick = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];
export function randomName() {
  const f = pick(FIRST), l = pick(LAST);
  return { citizenName: `${f} ${l}`, handle: `${f.toLowerCase()}${l[0].toLowerCase()}` };
}
export const RESERVED = ['vitalik', 'vitalik buterin', 'buterin', 'emerald', 'gladias', 'tapaia', 'team', 'admin', 'moderator', 'mod', 'support', 'staff', 'tapaiasquare', 'zipcoin', 'zipcoinbook'];
