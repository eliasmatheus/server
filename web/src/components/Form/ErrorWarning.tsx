export function ErrorWarning({ children }: { children: string }) {
  return <span className="text-sm text-red-500 italic">{children}</span>;
}
