// Room access rules (spec F3). Enforced on the server; the client uses the same rules to show locks.
import type { Channel, PublicUser } from './types';

const OPEN_TO_VISITORS = ['lobby', 'announcements'];
const OPEN_TO_SIGNED_IN = ['lobby', 'support', 'announcements'];

export function canRead(u: PublicUser | null | undefined, ch: Channel): boolean {
  if (ch.layer === 'dm') return !!u && !!ch.members?.includes(u.id);
  if (!u) return OPEN_TO_VISITORS.includes(ch.id);
  if (!u.isCitizen) return OPEN_TO_SIGNED_IN.includes(ch.id);
  return true;
}

export function canPost(u: PublicUser | null | undefined, ch: Channel): boolean {
  if (!u) return false;
  if (u.badges.includes('bot')) return ch.id === 'feeds';
  if (ch.layer === 'dm') return !!ch.members?.includes(u.id);
  if (ch.id === 'announcements' || ch.id === 'dev-updates') return u.badges.includes('team');
  if (ch.id === 'feeds') return false;
  if (!u.isCitizen) return ch.id === 'lobby' || ch.id === 'support';
  return true;
}

export function postBlockedReason(u: PublicUser | null | undefined, ch: Channel): string {
  if (!u) return 'Sign in to post.';
  if (ch.id === 'announcements') return '#announcements is read-only. Only the team posts here.';
  if (ch.id === 'dev-updates') return 'Only the team posts in #dev-updates.';
  if (ch.id === 'feeds') return '#feeds is for read-only bots.';
  if (!u.isCitizen) return 'Become a citizen to post here.';
  return 'You can’t post here.';
}

export const byteLen = (s: string) => new TextEncoder().encode(s).length;
