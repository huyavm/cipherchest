import { NavLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/accounts', label: 'Accounts' },
  { to: '/tools', label: 'Tools' },
  { to: '/backup', label: 'Backup' }
];

export const Sidebar = () => {
  const { logout } = useAuth();
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
      <div className="p-6 text-xl font-semibold">CipherChest</div>
      <nav className="flex-1 px-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `block px-3 py-2 rounded transition ${isActive ? 'bg-brand-500 text-white' : 'text-slate-300 hover:bg-slate-800'}`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
      <button
        className="m-4 bg-slate-800 hover:bg-slate-700 text-sm py-2 rounded"
        onClick={logout}
      >
        Logout
      </button>
    </aside>
  );
};
