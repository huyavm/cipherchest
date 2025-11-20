import { useEffect } from 'react';
import { useAuth } from './useAuth';

const IDLE_MINUTES = 15;

export const useAutoLogout = () => {
  const { logout, token } = useAuth();

  useEffect(() => {
    if (!token) return;
    let timer: number;

    const reset = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => {
        logout();
      }, IDLE_MINUTES * 60 * 1000);
    };

    ['click', 'mousemove', 'keydown'].forEach((evt) => document.addEventListener(evt, reset));
    reset();
    return () => {
      window.clearTimeout(timer);
      ['click', 'mousemove', 'keydown'].forEach((evt) => document.removeEventListener(evt, reset));
    };
  }, [logout, token]);
};
