import { useNavigate } from 'react-router-dom';
import { ButtonHTMLAttributes } from 'react';
import { BiChevronLeft } from 'react-icons/bi';

interface LinkButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {}

export function GoBackButton(props: LinkButtonProps) {
  const navigate = useNavigate();

  return (
    <button
      {...props}
      onClick={() => navigate(-1)}
      className="group flex font-semibold text-sm leading-6 text-slate-700 hover:text-slate-900 dark:text-slate-200 dark:hover:text-white"
    >
      <BiChevronLeft className="text-lg mr-1 text-slate-400 w-auto h-6 group-hover:text-slate-600 dark:group-hover:text-slate-300" />
      Go back
    </button>
  );
}
