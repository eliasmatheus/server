import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import parse from 'html-react-parser';
import { BiChevronLeft, BiEditAlt, BiTrash } from 'react-icons/bi';

import Header from '../components/Header';
import api from '../services/api';
import date from '../utils/date-formatter';
import { Button } from '../components/Buttons/Button';
import { useToast } from '../hooks/toast';
import { LinkButton } from '../components/Buttons/LinkButton';

export interface IArticle {
  id: string;
  title: string;
  subtitle: string;
  author_id: number;
  author: unknown;
  content: string;
  created_at: string;
}

function Article() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [loadingDelete, setLoadingDelete] = useState(false);
  const [article, setArticle] = useState<any>();

  useEffect(() => {
    api.get(`/article/${id}`).then(response => {
      setArticle(response.data);
    });
  }, []);

  function handleDeleteArticle() {
    if (window.confirm('Are you sure you want to delete this article?')) {
      setLoadingDelete(true);

      // Simula o tempo de espera para a requisição
      setTimeout(() => {
        deleteArticle();
      }, 2000);
    }
  }

  async function deleteArticle() {
    setLoadingDelete(true);

    try {
      await api.delete(`/article/${id}`);

      addToast({
        type: 'success',
        title: `Article deleted successfully!`,
      });

      setLoadingDelete(false);

      navigate('/');
    } catch (error) {
      setLoadingDelete(false);

      addToast({
        type: 'error',
        title: 'Error deleting article!',
        description: 'Please try again',
      });
    }
  }

  return (
    <>
      <Header />

      <div className="overflow-hidden">
        <div className="max-w-8xl mx-auto">
          <div className="flex px-4 pt-8 pb-10 lg:px-8">
            <LinkButton to="/">
              <BiChevronLeft className="text-lg mr-1 text-slate-400 w-auto h-6 group-hover:text-slate-600 dark:group-hover:text-slate-300" />
              Go back
            </LinkButton>
          </div>
        </div>

        <div className="px-4 pb-28 sm:px-6 md:px-8">
          <div className="max-w-3xl mx-auto">
            <main>
              {article && (
                <article className="relative pt-10">
                  {/* Título do Artigo */}
                  <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-slate-200 md:text-3xl">
                    {article.title}
                  </h1>

                  {/* Botões de edição e exclusão (position: absolute) */}
                  <div className="absolute z-10 top-0 right-0 placeholder:flex space-x-2">
                    <Button
                      color="alternative"
                      onClick={() => navigate(`/edit-article/${id}`)}
                    >
                      <div className="flex">
                        <BiEditAlt className="text-lg" />
                      </div>
                    </Button>

                    <Button
                      color="alternative"
                      onClick={handleDeleteArticle}
                      loading={loadingDelete}
                    >
                      <BiTrash className=" text-lg" />
                    </Button>
                  </div>

                  {/* Data do artigo (position: absolute) */}
                  <div className="text-sm leading-6">
                    <dl>
                      <dt className="sr-only">Date</dt>
                      <dd className="absolute top-0 inset-x-0 text-slate-700 dark:text-slate-400">
                        <time dateTime={article.created_at}>
                          {date(article.created_at)}
                        </time>
                      </dd>
                    </dl>
                  </div>

                  <div className="mt-6 flex justify-between">
                    <ul className="flex flex-wrap text-sm leading-6 -mt-6 -mx-5">
                      <li className="flex items-center font-medium whitespace-nowrap px-5 mt-6">
                        {article.author?.avatar_url && (
                          <div className="mr-3 w-9 h-9 rounded-full bg-slate-50 dark:bg-slate-800">
                            <img
                              src={
                                article.author.avatar_url ||
                                '/images/avatar-placeholder.png'
                              }
                              alt=""
                              className="mr-3 w-9 h-9 rounded-full aspect-square object-cover bg-slate-50 dark:bg-slate-800"
                              decoding="async"
                            />
                          </div>
                        )}

                        <div className="text-sm leading-4">
                          <div className="text-slate-900 dark:text-slate-200">
                            {article.author?.first_name} {article.author?.last_name}
                          </div>

                          {article.author?.twitter_username && (
                            <div className="mt-1">
                              <a
                                href={`https://twitter.com/${article.author.twitter_username}`}
                                className="text-sky-500 hover:text-sky-600 dar:text-sky-400"
                                target="_blank"
                                rel="noreferrer noopener"
                              >
                                @{article.author.twitter_username}
                              </a>
                            </div>
                          )}
                        </div>
                      </li>
                    </ul>
                  </div>

                  <div className="mt-12 prose prose-slate dark:prose-dark">
                    <div className="my-8">
                      {/* <div className="relative not-prose my-[2em] first:mt-0 last:mb-0 rounded-2xl overflow-hidden">
                        <img
                          src="https://tailwindcss.com/_next/static/media/card.bd99fd56.jpg"
                          alt="Tailwind CSS v3.3"
                        />

                        <div className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-slate-900/10 dark:ring-white/10"></div>
                      </div> */}

                      <p>{article.subtitle}</p>

                      {parse(article.content)}
                    </div>
                  </div>
                </article>
              )}
            </main>
          </div>
        </div>
      </div>
    </>
  );
}

export default Article;
