import { InputHTMLAttributes } from 'react';
import { Path, UseFormRegister } from 'react-hook-form';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: Path<any>;
  register: UseFormRegister<any>;
  required?: boolean;
}

export function Input({ label, register, required, ...props }: InputProps) {
  return (
    <input
      {...register(label, { required })}
      {...props}
      className="
        appearance-none 
        shadow 
        rounded-md 
        block
        ring-1 ring-slate-900/5 dark:ring-slate-200/20
        leading-5 
        sm:text-sm 
        border border-transparent
        py-2 px-3
        w-full
        text-slate-900 focus:outline-none focus-ring-2 focus:ring-sky-500 dark:focus:ring-sky-500
        bg-white dark:bg-slate-700/20
        dark:text-white
        placeholder:text-slate-400
      "
    />
  );
}
