import { useS } from '../store';

export function Legal({ className = 'legal-mini', short = false }: { className?: string; short?: boolean }) {
  const cfg = useS((s) => s.config);
  if (short) return (
    <div className={className}>
      Based on <i>Snowmoon</i> by Vitalik Buterin (GPL v3). Not affiliated with him, zipcoin.cash or Stockereum. Staff never DM first.
      {' '}<a href="https://x.com/TapaiaSquare" target="_blank" rel="noreferrer">@TapaiaSquare</a>
      {cfg && <> · build <a href={`${cfg.repoUrl}/commit/${cfg.build}`} target="_blank" rel="noreferrer">{cfg.build}</a></>}
    </div>
  );
  return (
    <div className={className}>
      Based on <i>Snowmoon</i> by Vitalik Buterin, used under GPL v3. Not affiliated with Vitalik Buterin, zipcoin.cash or Stockereum. Staff never DM first and never ask for your seed phrase.
      {' '}<a href="https://x.com/TapaiaSquare" target="_blank" rel="noreferrer">@TapaiaSquare</a> on X
      {cfg && <> · build <a href={`${cfg.repoUrl}/commit/${cfg.build}`} target="_blank" rel="noreferrer">{cfg.build}</a></>} · prototype
    </div>
  );
}
