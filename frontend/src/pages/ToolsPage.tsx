import { useState } from 'react';
import api from '../api';

export const ToolsPage = () => {
  const [passwordLength, setPasswordLength] = useState(16);
  const [generatedPassword, setGeneratedPassword] = useState('');
  const [totpSecret, setTotpSecret] = useState<any>(null);
  const [hibpStatus, setHibpStatus] = useState<string>('');
  const [hibpPassword, setHibpPassword] = useState('');

  const runPasswordGenerator = async () => {
    const { data } = await api.post('/tools/password', null, { params: { length: passwordLength } });
    setGeneratedPassword(data.password);
  };

  const runTotp = async () => {
    const { data } = await api.post('/tools/totp', null, { params: { account_name: 'CipherChest', issuer: 'CipherChest' } });
    setTotpSecret(data);
  };

  const runHibp = async () => {
    setHibpStatus('checking...');
    const { data } = await api.post('/tools/hibp', null, { params: { password: hibpPassword } });
    setHibpStatus(data.pwned ? 'Password found in breaches!' : 'Password safe.');
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Security Tools</h1>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-slate-900 rounded p-4 space-y-3">
          <h2 className="font-semibold">Password Generator</h2>
          <input type="range" min="12" max="32" value={passwordLength} onChange={(e) => setPasswordLength(parseInt(e.target.value))} />
          <div className="text-sm">Length: {passwordLength}</div>
          <button className="bg-brand-500 px-4 py-2 rounded" onClick={runPasswordGenerator}>Generate</button>
          {generatedPassword && <code className="block bg-slate-800 p-2 rounded break-all">{generatedPassword}</code>}
        </div>
        <div className="bg-slate-900 rounded p-4 space-y-3">
          <h2 className="font-semibold">TOTP Secret</h2>
          <button className="bg-brand-500 px-4 py-2 rounded" onClick={runTotp}>Generate Secret</button>
          {totpSecret && (
            <div className="space-y-2">
              <div>Secret: <code>{totpSecret.secret}</code></div>
              <img src={`data:image/png;base64,${totpSecret.qr_base64}`} alt="TOTP QR" className="w-40" />
            </div>
          )}
        </div>
        <div className="bg-slate-900 rounded p-4 space-y-3">
          <h2 className="font-semibold">Have I Been Pwned</h2>
          <input type="password" placeholder="Password" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={hibpPassword} onChange={(e) => setHibpPassword(e.target.value)} />
          <button className="bg-brand-500 px-4 py-2 rounded" onClick={runHibp}>Check</button>
          {hibpStatus && <div>{hibpStatus}</div>}
        </div>
      </div>
    </div>
  );
};
