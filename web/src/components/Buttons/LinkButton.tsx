import { Link, LinkProps } from 'react-router-dom';

interface LinkButtonProps extends LinkProps {
  children: React.ReactNode;
}

export function LinkButton({ children, ...props }: LinkButtonProps) {
  return (
    <Link
      {...props}
      className="group flex font-semibold text-sm leading-6 text-slate-700 hover:text-slate-900 dark:text-slate-200 dark:hover:text-white"
    >
      {children}
    </Link>
  );
}
