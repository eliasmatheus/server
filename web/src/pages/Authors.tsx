import { useEffect, useState } from 'react';
import Header from '../components/Header';
import api from '../services/api';
import '../styles/main.css';
import { Button } from '../components/Buttons/Button';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import Main from '../components/Main';
import { BiChevronRight } from 'react-icons/bi';

export interface IAuthorPreview {
  id: number;
  first_name: string;
  last_name: string;
  twitter_username: string;
  created_at: string;
  avatar_url: string;
  articles_count: number;
}

function Authors() {
  const navigate = useNavigate();
  const [authors, setAuthors] = useState<IAuthorPreview[]>([]);

  useEffect(() => {
    api.get('/authors').then(response => {
      setAuthors(response.data.authors);
    });
  }, []);

  return (
    <>
      <Header />

      <Hero
        className="bg-bottom"
        backgroundUrl="https://images.unsplash.com/photo-1508780709619-79562169bc64?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
      >
        {/* text-slate-900 */}
        <h1 className="mb-4 text-3xl tracking-tight text-slate-200 font-extrabold dark:text-slate-200">
          Our Authors
        </h1>

        {/* text-slate-700 */}
        <p className="mb-4 text-lg text-slate-400 dark:text-slate-400">
          Meet the authors who make Code Chronicles possible.
        </p>

        <Button color="default" onClick={() => navigate('/new-author')}>
          Add Author
        </Button>
      </Hero>

      <Main>
        <div className="mt-3 max-w-4xl sm:mx-auto sm:px-4">
          <div className="space-y-16">
            <ul className="grid grid-cols-1 gap-x-16 gap-y-8 xl:grid-cols-2 xl:gap-y-10">
              {authors &&
                authors.map(author => (
                  <li key={author.id} className="relative flex items-start">
                    <div className="z-20 w-16 h-16 p-[0.1875rem] rounded-full ring-1 ring-slate-900/10 shadow overflow-hidden flex-none dark:bg-sky-500 dark:highlight-white/20">
                      <div className="aspect-w-1 aspect-h-1 bg-[length:100%]">
                        <img
                          src={author.avatar_url || '/images/avatar-placeholder.png'}
                          alt=""
                          className="rounded-full aspect-square object-cover bg-slate-50 dark:bg-slate-800"
                          decoding="async"
                        />
                      </div>
                    </div>
                    <div className="peer z-20 group flex-auto ml-6">
                      <h3 className="mb-0 font-semibold text-slate-900 dark:text-slate-200">
                        <a
                          className="before:absolute before:-inset-3 before:rounded-2xl sm:before:-inset-4"
                          href={`/edit-author/${author.id}`}
                        >
                          {author.first_name} {author.last_name}
                          <BiChevronRight
                            size={20}
                            className="ml-1 w-auto overflow-visible inline -mt-px text-slate-400 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100"
                          />
                        </a>
                      </h3>

                      <div className="mb-1 z-20">
                        <a
                          href={`https://twitter.com/${author.twitter_username}`}
                          className="text-sky-500 hover:text-sky-600 dar:text-sky-400"
                          target="_blank"
                          rel="noreferrer noopener"
                        >
                          @{author.twitter_username}
                        </a>
                      </div>

                      <div className="prose prose-slate prose-sm text-slate-600 dark:prose-dark">
                        <p>Articles: {author.articles_count}</p>
                      </div>
                    </div>
                    <div className="absolute z-10 -inset-3 rounded-2xl bg-slate-50 dark:bg-slate-800/50 opacity-0 peer-hover:opacity-100 sm:-inset-4"></div>
                  </li>
                ))}
            </ul>
          </div>
        </div>

        {authors.length === 0 && (
          <div className="py-16 sm:text-center text-slate-700 dark:text-slate-400">
            <h3 className="text-lg">No posts yet.</h3>
            <p className="text-base ">Click on Add New to create one</p>
          </div>
        )}
      </Main>
    </>
  );
}

export default Authors;
