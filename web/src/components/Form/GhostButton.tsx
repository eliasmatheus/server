import { ButtonHTMLAttributes } from 'react';
import { BASIC_BUTTON_CLASS } from '../Buttons/Button';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  status?: 'danger' | 'primary';
}

export function GhostButton(props: ButtonProps) {
  if (!props.status) {
    props.status = 'primary';
  }

  const colors = {
    danger:
      'hover:bg-red-600 dark:hover:bg-red-400 dark:hover:ring-red-500 dark:hover:text-red-900',
    primary:
      'hover:bg-sky-600 dark:hover:bg-sky-400 dark:hover:ring-sky-500 dark:hover:text-sky-900',
  };

  return (
    <button
      {...props}
      className={`
        ${BASIC_BUTTON_CLASS}
        ring-1 ring-slate-900/5 
        text-slate-900 dark:text-white
        ${colors[props.status]}
        bg-white dark:bg-slate-700/20 
        dark:ring-slate-200/20 
      `}
    ></button>
  );
}
