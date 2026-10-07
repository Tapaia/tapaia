// The shared Meldan clock (spec F4.7): 100 ticks per minute, 100 minutes per longhour,
// 10 longhours per day, tick 00000 at midnight UTC. One day = 100,000 ticks.
export const TICKS_PER_DAY = 100_000;

export function meldanTicks(t: number | Date = Date.now()): number {
  const ms = typeof t === 'number' ? t : t.getTime();
  const msOfDay = ((ms % 86_400_000) + 86_400_000) % 86_400_000;
  return Math.floor((msOfDay / 86_400_000) * TICKS_PER_DAY);
}
export const fmtTicks = (n: number) => String(n).padStart(5, '0');
export const longhours = (ticks: number) => Math.floor(ticks / 10_000);
