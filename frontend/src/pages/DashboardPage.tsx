import { useEffect, useState } from 'react';
import api from '../api';

type Stats = {
  total_accounts: number;
  expiring_accounts: number;
  without_two_fa: number;
  by_category: Record<string, number>;
};

export const DashboardPage = () => {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    api.get('/dashboard/stats').then(({ data }) => setStats(data));
  }, []);

  if (!stats) return <div>Loading dashboard...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Security Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 rounded p-4">
          <p className="text-sm uppercase text-slate-400">Total Accounts</p>
          <p className="text-3xl font-bold">{stats.total_accounts}</p>
        </div>
        <div className="bg-slate-900 rounded p-4">
          <p className="text-sm uppercase text-slate-400">Expiring soon</p>
          <p className="text-3xl font-bold">{stats.expiring_accounts}</p>
        </div>
        <div className="bg-slate-900 rounded p-4">
          <p className="text-sm uppercase text-slate-400">Without 2FA</p>
          <p className="text-3xl font-bold">{stats.without_two_fa}</p>
        </div>
      </div>
      <div className="bg-slate-900 rounded p-4">
        <p className="text-sm uppercase text-slate-400 mb-2">By Category</p>
        <div className="space-y-2">
          {Object.entries(stats.by_category).map(([category, count]) => (
            <div key={category} className="flex justify-between text-sm">
              <span>{category}</span>
              <span>{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
