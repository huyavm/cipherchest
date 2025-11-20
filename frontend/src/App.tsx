import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { AccountsPage } from './pages/AccountsPage';
import { ToolsPage } from './pages/ToolsPage';
import { BackupPage } from './pages/BackupPage';
import { AuthPage } from './pages/AuthPage';

const PrivateRoutes = () => {
  const { token } = useAuth();
  if (!token) {
    return <AuthPage />;
  }
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/accounts" element={<AccountsPage />} />
        <Route path="/tools" element={<ToolsPage />} />
        <Route path="/backup" element={<BackupPage />} />
      </Routes>
    </Layout>
  );
};

const App = () => (
  <AuthProvider>
    <BrowserRouter>
      <PrivateRoutes />
    </BrowserRouter>
  </AuthProvider>
);

export default App;
