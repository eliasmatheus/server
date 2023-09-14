interface HeroProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  backgroundUrl?: string;
}

export default function Hero({ children, backgroundUrl, className, ...rest }: HeroProps) {
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  console.log(`${mq.matches ? 'dark' : 'light'} mode`);

  return (
    <header
      className={`pt-32 pb-60 sm:text-center bg-no-repeat bg-cover flex justify-center items-center ${className}`}
      style={{
        backgroundImage: `url(${backgroundUrl})`,
      }}
      {...rest}
    >
      <div className="bg-slate-900/40 w-fit p-12 backdrop-blur-md rounded-xl">
        {children}
      </div>
    </header>
  );
}
