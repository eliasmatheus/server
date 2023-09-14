import { useEffect, useState } from 'react';
import ArticlePreview from '../components/ArticlePreview';
import Footer from '../components/Footer';
import Header from '../components/Header';
import api from '../services/api';
import '../styles/main.css';
import { Button } from '../components/Buttons/Button';
import { useNavigate } from 'react-router-dom';
import Hero from '../components/Hero';
import Main from '../components/Main';

interface IArticlePreview {
  id: number;
  title: string;
  subtitle: string;
  author: string;
  created_at: string;
}

function Articles() {
  const navigate = useNavigate();
  const [articles, setArticles] = useState<IArticlePreview[]>([]);

  useEffect(() => {
    api.get('/articles').then(response => {
      setArticles(response.data.articles);
    });
  }, []);

  return (
    <>
      <Header />

      <Hero
        className="bg-top"
        backgroundUrl="https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
      >
        {/* text-slate-900 */}
        <h1 className="mb-4 text-3xl tracking-tight text-slate-200 font-extrabold dark:text-slate-200">
          Code Chronicles
        </h1>

        {/* text-slate-700 */}
        <p className="mb-4 text-lg text-slate-400 dark:text-slate-400">
          Stay up-to-date with our latest programming insights and discoveries.
        </p>

        <Button color="default" onClick={() => navigate('/new-article')}>
          Create Article
        </Button>
      </Hero>

      <Main>
        <div className="relative mt-10 sm:pb-12 sm:ml-[calc(2rem+1px)] md:ml-[calc(3.5rem+1px)] lg:ml-[max(calc(14.5rem+1px),calc(100%-48rem))]">
          <div className="hidden absolute top-3 bottom-0 right-full mr-7 md:mr-[3.25rem] w-px bg-slate-200 dark:bg-slate-800 sm:block"></div>

          <div className="space-y-16">
            {articles &&
              articles.map(article => {
                return <ArticlePreview key={article.id} {...article} />;
              })}
          </div>
        </div>

        {articles.length === 0 && (
          <div className="py-16 sm:text-center text-slate-700 dark:text-slate-400">
            <h3 className="text-lg">No posts yet.</h3>
            <p className="text-base ">Click on Add New to create one</p>
          </div>
        )}
      </Main>
    </>
  );
}

export default Articles;
