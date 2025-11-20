import { useState } from 'react';
import api from '../api';

export const BackupPage = () => {
  const [passphrase, setPassphrase] = useState('');
  const [exported, setExported] = useState('');
  const [importPayload, setImportPayload] = useState('');
  const [csvType, setCsvType] = useState('email');
  const [csvContent, setCsvContent] = useState('');

  const runExport = async () => {
    const { data } = await api.post('/backup/export', { passphrase });
    setExported(data.payload);
  };

  const runImport = async () => {
    await api.post('/backup/import', { passphrase, payload: importPayload });
    alert('Backup restored');
  };

  const runCsv = async () => {
    const { data } = await api.get(`/backup/csv/${csvType}`, { responseType: 'text' });
    setCsvContent(data);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Backup & Restore</h1>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-slate-900 rounded p-4 space-y-3">
          <h2 className="font-semibold">Export encrypted backup</h2>
          <input type="password" placeholder="Passphrase" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={passphrase} onChange={(e) => setPassphrase(e.target.value)} />
          <button className="bg-brand-500 px-4 py-2 rounded" onClick={runExport}>Create backup</button>
          {exported && <textarea className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" rows={4} value={exported} readOnly />}
        </div>
        <div className="bg-slate-900 rounded p-4 space-y-3">
          <h2 className="font-semibold">Restore backup</h2>
          <textarea className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" rows={4} value={importPayload} onChange={(e) => setImportPayload(e.target.value)} placeholder="Paste encrypted payload" />
          <button className="bg-brand-500 px-4 py-2 rounded" onClick={runImport}>Restore</button>
        </div>
      </div>
      <div className="bg-slate-900 rounded p-4 space-y-3">
        <h2 className="font-semibold">Export CSV</h2>
        <select className="bg-slate-800 border border-slate-700 rounded px-3 py-2" value={csvType} onChange={(e) => setCsvType(e.target.value)}>
          <option value="email">Email</option>
          <option value="web">Web</option>
          <option value="cloud">Cloud</option>
          <option value="payment">Payment</option>
          <option value="other">Other</option>
        </select>
        <button className="bg-brand-500 px-4 py-2 rounded" onClick={runCsv}>Export CSV</button>
        {csvContent && <textarea className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" rows={6} value={csvContent} readOnly />}
      </div>
    </div>
  );
};
