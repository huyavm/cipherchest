import { useEffect, useMemo, useState } from 'react';
import api from '../api';

type Account = {
  id: number;
  service_name: string;
  provider: string;
  account_type: string;
  tags: string[];
  status: string;
  metadata: Record<string, any>;
  notes?: string;
  sensitive: any;
};

const defaultSensitive = () => ({
  login_email: '',
  password: '',
  two_fa_secret: '',
  recovery_email: ''
});

export const AccountsPage = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [search, setSearch] = useState('');
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Account | null>(null);
  const [activeTab, setActiveTab] = useState<'login' | 'security' | 'notes' | 'attachments'>('login');
  const [confirmId, setConfirmId] = useState<number | null>(null);
  const [attachments, setAttachments] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const apiOrigin = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}` : '';
  const [form, setForm] = useState<any>({
    service_name: '',
    provider: '',
    account_type: 'email',
    tags: [],
    status: 'active',
    notes: '',
    sensitive: defaultSensitive()
  });
  const tabOptions: { id: 'login' | 'security' | 'notes' | 'attachments'; label: string }[] = [
    { id: 'login', label: 'Login' },
    { id: 'security', label: '2FA & Security' },
    { id: 'attachments', label: 'Attachments' },
    { id: 'notes', label: 'Notes' }
  ];

  const load = () => {
    api.get('/accounts', { params: { search } }).then(({ data }) => setAccounts(data));
  };

  useEffect(() => {
    load();
  }, []);

  const fetchAttachments = async (accountId: number) => {
    const { data } = await api.get(`/attachments/accounts/${accountId}`);
    setAttachments(data);
  };

  const openForm = (account?: Account) => {
    if (account) {
      setEditing(account);
      setForm({ ...account, tags: account.tags, sensitive: { ...defaultSensitive(), ...account.sensitive } });
      fetchAttachments(account.id);
    } else {
      setEditing(null);
      setForm({ service_name: '', provider: '', account_type: 'email', tags: [], status: 'active', notes: '', sensitive: defaultSensitive() });
      setAttachments([]);
    }
    setActiveTab('login');
    setFormOpen(true);
  };

  const submit = async () => {
    if (editing) {
      await api.put(`/accounts/${editing.id}`, form);
    } else {
      await api.post('/accounts', form);
    }
    setFormOpen(false);
    load();
  };

  const destroy = async (id: number) => {
    await api.delete(`/accounts/${id}`);
    load();
    setConfirmId(null);
  };

  const handleUpload = async (files: FileList | null) => {
    if (!editing || !files || !files.length) return;
    const formData = new FormData();
    formData.append('upload', files[0]);
    setUploading(true);
    await api.post(`/attachments/accounts/${editing.id}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    setUploading(false);
    fetchAttachments(editing.id);
  };

  const removeAttachment = async (id: number) => {
    await api.delete(`/attachments/${id}`);
    if (editing) fetchAttachments(editing.id);
  };

  const filtered = useMemo(() => {
    if (!search) return accounts;
    return accounts.filter((acc) => acc.service_name.toLowerCase().includes(search.toLowerCase()));
  }, [accounts, search]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Accounts</h1>
        <button className="bg-brand-500 text-white px-4 py-2 rounded" onClick={() => openForm()}>
          Add account
        </button>
      </div>
      <div className="bg-slate-900 rounded p-4 space-y-3">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search service or provider"
          className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2"
        />
        <button className="text-sm text-brand-500" onClick={load}>Run search</button>
      </div>
      <div className="bg-slate-900 rounded overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-800 text-xs uppercase text-slate-400">
            <tr>
              <th className="p-3">Service</th>
              <th className="p-3">Provider</th>
              <th className="p-3">Type</th>
              <th className="p-3">Status</th>
              <th className="p-3">Tags</th>
              <th className="p-3" />
            </tr>
          </thead>
          <tbody>
            {filtered.map((account) => (
              <tr key={account.id} className="border-t border-slate-800 text-sm">
                <td className="p-3">{account.service_name}</td>
                <td className="p-3">{account.provider}</td>
                <td className="p-3 capitalize">{account.account_type}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-xs ${account.status === 'active' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                    {account.status}
                  </span>
                </td>
                <td className="p-3 space-x-1">
                  {account.tags.map((tag) => (
                    <span key={tag} className="px-2 py-0.5 rounded-full bg-slate-800 text-xs">{tag}</span>
                  ))}
                </td>
                <td className="p-3 space-x-2">
                  <button className="text-brand-400" onClick={() => openForm(account)}>Edit</button>
                  <button className="text-red-400" onClick={() => setConfirmId(account.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="p-4 text-center text-slate-500">No accounts yet</div>}
      </div>

      {formOpen && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-slate-900 rounded shadow-xl w-full max-w-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
              <h2 className="text-lg font-semibold">{editing ? 'Update Account' : 'Add New Account'}</h2>
              <button onClick={() => setFormOpen(false)}>✕</button>
            </div>
            <div className="px-4 pt-4 flex space-x-2 border-b border-slate-800">
              {tabOptions.map((tab) => (
                <button
                  key={tab.id}
                  className={`px-3 py-2 rounded ${activeTab === tab.id ? 'bg-brand-500' : 'bg-slate-800'}`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              ))}
            </div>
            <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              {activeTab === 'login' && (
                <>
                  <label className="space-y-1 text-sm">
                    <span>Service Name</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.service_name} onChange={(e) => setForm({ ...form, service_name: e.target.value })} />
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>Provider</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.provider} onChange={(e) => setForm({ ...form, provider: e.target.value })} />
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>Type</span>
                    <select className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.account_type} onChange={(e) => setForm({ ...form, account_type: e.target.value })}>
                      <option value="email">Email</option>
                      <option value="web">Web</option>
                      <option value="cloud">Cloud</option>
                      <option value="payment">Payment</option>
                      <option value="other">Other</option>
                    </select>
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>Status</span>
                    <select className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
                      <option value="active">Active</option>
                      <option value="suspended">Suspended</option>
                    </select>
                  </label>
                  <label className="space-y-1 text-sm col-span-full">
                    <span>Tags (comma separated)</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.tags.join(',')} onChange={(e) => setForm({ ...form, tags: e.target.value.split(',').map((t) => t.trim()).filter(Boolean) })} />
                  </label>
                </>
              )}
              {activeTab === 'security' && (
                <>
                  <label className="space-y-1 text-sm">
                    <span>Login Email</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.sensitive.login_email} onChange={(e) => setForm({ ...form, sensitive: { ...form.sensitive, login_email: e.target.value } })} />
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>Password</span>
                    <input type="password" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.sensitive.password} onChange={(e) => setForm({ ...form, sensitive: { ...form.sensitive, password: e.target.value } })} />
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>Recovery Email</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.sensitive.recovery_email} onChange={(e) => setForm({ ...form, sensitive: { ...form.sensitive, recovery_email: e.target.value } })} />
                  </label>
                  <label className="space-y-1 text-sm">
                    <span>2FA Secret</span>
                    <input className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.sensitive.two_fa_secret} onChange={(e) => setForm({ ...form, sensitive: { ...form.sensitive, two_fa_secret: e.target.value } })} />
                  </label>
                </>
              )}
              {activeTab === 'notes' && (
                <label className="space-y-1 text-sm col-span-full">
                  <span>Notes</span>
                  <textarea className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
                </label>
              )}
              {activeTab === 'attachments' && (
                <div className="space-y-3 col-span-full">
                  {editing ? (
                    <>
                      <label className="space-y-1 text-sm block">
                        <span>Upload encrypted file (PDF, image, invoices)</span>
                        <input type="file" onChange={(e) => handleUpload(e.target.files)} className="w-full text-sm" />
                      </label>
                      {uploading && <p className="text-xs text-slate-400">Encrypting & uploading...</p>}
                      <div className="space-y-2">
                        {attachments.map((file) => (
                          <div key={file.id} className="flex items-center justify-between bg-slate-800 rounded px-3 py-2 text-sm">
                            <div>
                              <p>{file.filename}</p>
                              <p className="text-xs text-slate-400">{new Date(file.created_at).toLocaleString()}</p>
                            </div>
                            <div className="flex space-x-2">
                              <a className="text-brand-400" href={`${apiOrigin}/api/attachments/${file.id}`} target="_blank" rel="noreferrer">Download</a>
                              <button className="text-red-400" onClick={() => removeAttachment(file.id)}>Delete</button>
                            </div>
                          </div>
                        ))}
                        {attachments.length === 0 && <p className="text-xs text-slate-500">No files yet.</p>}
                      </div>
                    </>
                  ) : (
                    <p className="text-sm text-slate-500">Save the account first to manage attachments.</p>
                  )}
                </div>
              )}
            </div>
            <div className="flex justify-end space-x-2 border-t border-slate-800 px-4 py-3">
              <button className="px-4 py-2" onClick={() => setFormOpen(false)}>Cancel</button>
              <button className="bg-brand-500 px-4 py-2 rounded" onClick={submit}>{editing ? 'Update' : 'Create'}</button>
            </div>
          </div>
        </div>
      )}

      {confirmId && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4">
          <div className="bg-slate-900 rounded p-6 space-y-4 w-full max-w-sm">
            <h3 className="text-lg font-semibold">Confirm deletion</h3>
            <p className="text-sm text-slate-400">This will permanently remove the selected account and its encrypted secrets.</p>
            <div className="flex justify-end space-x-2">
              <button className="px-4 py-2" onClick={() => setConfirmId(null)}>Cancel</button>
              <button className="bg-red-500 px-4 py-2 rounded" onClick={() => destroy(confirmId)}>Delete</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
