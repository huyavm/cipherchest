import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export const AuthPage = () => {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');

  const submit = async () => {
    try {
      setError('');
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(fullName, email, password);
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100">
      <div className="bg-slate-900 rounded shadow-xl p-8 w-full max-w-md space-y-4">
        <div className="flex space-x-2">
          <button className={`flex-1 py-2 rounded ${mode === 'login' ? 'bg-brand-500' : 'bg-slate-800'}`} onClick={() => setMode('login')}>Login</button>
          <button className={`flex-1 py-2 rounded ${mode === 'register' ? 'bg-brand-500' : 'bg-slate-800'}`} onClick={() => setMode('register')}>Register</button>
        </div>
        {mode === 'register' && (
          <input placeholder="Full name" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        )}
        <input placeholder="Email" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button className="w-full bg-brand-500 rounded py-2" onClick={submit}>
          {mode === 'login' ? 'Sign in' : 'Create account'}
        </button>
      </div>
    </div>
  );
};
