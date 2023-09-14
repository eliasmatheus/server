import { Link } from 'react-router-dom';
import date from '../utils/date-formatter';

interface ArticlePreviewData {
  id: number;
  title: string;
  subtitle: string;
  author: string;
  created_at: string;
}

function ArticlePreview(props: ArticlePreviewData) {
  const articleURL = `/article/${props.id}`;

  return (
    <article className="relative group">
      <div className="absolute -inset-y-2.5 -inset-x-4 md:-inset-y-4 md:-inset-x-6 sm:rounded-2xl group-hover:bg-slate-50/70 dark:group-hover:bg-slate-800/50"></div>
      <svg
        viewBox="0 0 9 9"
        className="hidden absolute right-full mr-6 top-2 text-slate-200 dark:text-slate-600 md:mr-12 w-[calc(0.5rem+1px)] h-[calc(0.5rem+1px)] overflow-visible sm:block"
      >
        <circle
          cx="4.5"
          cy="4.5"
          r="4.5"
          stroke="currentColor"
          className="fill-white dark:fill-slate-900"
          strokeWidth="2"
        ></circle>
      </svg>

      <div className="relative">
        <h3 className="text-base font-semibold tracking-tight text-slate-900 dark:text-slate-200 pt-8 lg:pt-0">
          {props.title}
        </h3>

        <div className="mt-2 mb-4 prose prose-slate prose-a:text-slate-900 prose-a:z-10 dark:prose-a:text-slate-200 line-clamp-2">
          <p>{props.subtitle}</p>
        </div>

        <dl className="absolute left-0 top-0 lg:left-auto lg:right-full lg:mr-[calc(6.5rem+1px)]">
          <dt className="sr-only">Date</dt>

          <dd className="whitespace-nowrap text-sm leading-6 dark:text-slate-400">
            {/* <time dateTime="2023-03-28T14:30:00.000Z">March 28, 2023</time> */}
            <time dateTime={props.created_at}>{date(props.created_at, 'shortDate')}</time>
          </dd>
        </dl>
      </div>

      <Link
        to={articleURL}
        className="flex items-center text-sm text-sky-500 font-medium"
      >
        <span className="absolute -inset-y-2.5 -inset-x-4 md:-inset-y-4 md:-inset-x-6 sm:rounded-2xl"></span>

        <span className="relative">
          Read more
          <span className="sr-only">, {props.subtitle}</span>
        </span>

        <svg
          className="relative mt-px overflow-visible ml-2.5 text-sky-300 dark:text-sky-700"
          width="3"
          height="6"
          viewBox="0 0 3 6"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M0 0L3 3L0 6"></path>
        </svg>
      </Link>
    </article>
  );
}

export default ArticlePreview;
