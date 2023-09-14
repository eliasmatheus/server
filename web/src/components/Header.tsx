import { Link, useLocation } from 'react-router-dom';

function Header() {
  const location = useLocation();

  return (
    <div
      className="
        sticky top-0 z-40 
        w-full 
        backdrop-blur 
        flex-none 
        transition-colors duration-500 
        lg:z-50 lg:border-b lg:border-slate-900/10
        dark:lg:border-slate-200/10 dark:border-slate-50/[0.06] 
        bg-white/95 supports-backdrop-blur:bg-white/60 
        dark:bg-transparent
    "
    >
      <div className="max-w-8xl mx-auto">
        <div className="py-4 border-b border-slate-900/10 lg:px-8 lg:border-0 dark:border-slate-300/10 px-4">
          <div className="relative flex items-center">
            <Link to="/" className="mr-3 flex-none overflow-hidden">
              <span className="sr-only">Code Chronicles home page</span>

              <span className="tracking-tight text-slate-900 dark:text-slate-100">
                Code Chronicles
              </span>
            </Link>

            <div className="relative hidden lg:flex items-center ml-auto">
              <nav className="text-sm leading-6 font-semibold text-slate-700 dark:text-slate-200">
                <ul className="flex space-x-8">
                  {/* <li>
                    <Link
                      to="/about"
                      className="hover:text-sky-500 dark:hover:text-sky-400"
                    >
                      About
                    </Link>
                  </li> */}

                  <li>
                    <Link
                      to="/articles"
                      className={`${
                        location.pathname === '/articles' && 'border-b-2 border-sky-600'
                      } hover:text-sky-500 dark:hover:text-sky-400`}
                    >
                      Articles
                    </Link>
                  </li>

                  <li>
                    <Link
                      to="/authors"
                      className={`${
                        location.pathname === '/authors' && 'border-b-2 border-sky-600'
                      } hover:text-sky-500 dark:hover:text-sky-400`}
                    >
                      Authors
                    </Link>
                  </li>
                </ul>
              </nav>

              {/* TODO: Adicionar botão de toggle de tema com Headless UI e links para redes sociais */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Header;
