interface MainProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export default function Main({ children, className, ...rest }: MainProps) {
  return (
    <main
      className={`max-w-[52rem] mx-auto mt-[-8rem] px-4 py-28 pt-16 sm:px-6 md:px-8 xl:px-12 lg:max-w-6xl bg-white dark:bg-slate-900 rounded-xl ${className}`}
      {...rest}
    >
      {children}
    </main>
  );
}
