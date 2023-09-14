import { ReactNode } from 'react';
import { ToastProvider } from './toast';

interface Props {
  children: ReactNode;
}

function AppProvider({ children }: Props) {
  return (
    <>
      <ToastProvider>{children}</ToastProvider>
    </>
  );
}

export default AppProvider;
