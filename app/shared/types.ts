import type { AvatarCfg } from './avatar';

export type Badge = 'founder' | 'onchain' | 'team' | 'mod' | 'bot';
export type Presence = 'here' | 'idle' | 'off';
export type Tile = 'c1' | 'c2' | 'c3' | 'c4' | 'c5' | 'c6';

export interface PublicUser {
  id: string;
  handle: string;          // OOC handle, used in community channels
  citizenName: string;     // IC name, used in Tapaia Square
  avatar: AvatarCfg;
  tile: Tile;
  badges: Badge[];
  isCitizen: boolean;
  entry?: 'founder' | 'burn';
  arrivalText?: string;
  arrivalAt?: number;
  wallet?: string;         // shortened
  kind: 'demo' | 'wallet' | 'seed' | 'bot';
  status?: string;
  presence: Presence;
  room?: string;
  linked: boolean;         // show handle + citizen name together
  about?: string;
  district?: string;
  createdAt: number;
  speaks: number;
  /** Zipcoin name label ("alice" = alice.zipcoin.cash). Real ones are resolved from the wallet via zipcoin.cash's API.
   *  demo: true = demo data or a simulated claim, NOT a real zipcoin.cash registration. */
  zip?: { name: string; demo?: boolean };
}

export type MsgKind = 'text' | 'system' | 'arrival' | 'speak';

export interface LinkCard { url: string; title: string; desc: string }

export interface Message {
  id: number;
  channel: string;
  userId?: string;
  kind: MsgKind;
  text: string;
  ts: number;
  replyTo?: number;
  reactions: Record<string, string[]>;
  card?: LinkCard;
  sys?: 'enter' | 'leave' | 'citizen';
  simulated?: boolean;     // demo burn: nothing burned
  sample?: boolean;        // sample/bot data, not real
  edited?: boolean;
  deleted?: boolean;
}

export interface Channel {
  id: string;
  name: string;
  layer: 'ooc' | 'ic' | 'dm';
  topic: string;
  pinned?: string;
  members?: string[];      // DMs only
}

export interface AppConfig {
  walletConnectProjectId: string | null;
  build: string;
  founderSlots: { total: number; used: number; demoValue: boolean };
  zcAddress: string;
  speakMinimum: number;
  repoUrl: string;
  zipcoin: { api: string; site: string };
}

export type ClientMsg =
  | { t: 'send'; channel: string; text: string; replyTo?: number; mode?: 'say' | 'speak' }
  | { t: 'react'; id: number; emoji: string }
  | { t: 'delete'; id: number }
  | { t: 'edit'; id: number; text: string }
  | { t: 'typing'; channel: string }
  | { t: 'room'; channel: string | null }
  | { t: 'presence'; state: 'here' | 'idle' }
  | { t: 'dm'; userId: string };

export type ServerMsg =
  | { t: 'hello'; me: PublicUser | null; users: PublicUser[]; channels: Channel[]; messages: Message[] }
  | { t: 'msg'; m: Message }
  | { t: 'update'; m: Message }
  | { t: 'user'; u: PublicUser }
  | { t: 'channel'; c: Channel; messages: Message[]; open?: boolean }
  | { t: 'typing'; channel: string; userId: string }
  | { t: 'error'; text: string };
