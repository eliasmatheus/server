import { TextareaHTMLAttributes } from 'react';
import { Path, UseFormRegister } from 'react-hook-form';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: Path<any>;
  register: UseFormRegister<any>;
  required?: boolean;
}

export function Textarea({ label, register, required, ...props }: TextareaProps) {
  return (
    <textarea
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
        tex-slate-900 focus:outline-none focus-ring-2 focus:ring-sky-500 dark:focus:ring-sky-500
        bg-white dark:bg-slate-700/20
        dark:text-white
        placeholder:text-slate-400
      "
    ></textarea>
  );
}
