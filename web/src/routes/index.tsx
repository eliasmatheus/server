import { Navigate, createBrowserRouter } from 'react-router-dom';
import Article from '../pages/Article';
import ArticleEditor from '../pages/ArticleEditor';
import Articles from '../pages/Articles';
import Authors from '../pages/Authors';
import AuthorForm from '../pages/AuthorForm';

const Router = createBrowserRouter([
  { path: '/', element: <Navigate to="/articles" /> },

  { path: '/articles', element: <Articles /> },
  { path: '/article/:id', element: <Article /> },
  { path: '/new-article', element: <ArticleEditor /> },
  { path: '/edit-article/:id', element: <ArticleEditor /> },

  { path: '/authors', element: <Authors /> },
  { path: '/new-author', element: <AuthorForm /> },
  { path: '/edit-author/:id', element: <AuthorForm /> },

  { path: '*', element: <Navigate to="/" /> },
]);

export default Router;
