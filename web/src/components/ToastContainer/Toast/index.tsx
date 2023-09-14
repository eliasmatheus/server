import React, { useEffect } from 'react';
import { FiAlertCircle, FiCheckCircle, FiInfo, FiXCircle } from 'react-icons/fi';
import { ToastMessage, useToast } from '../../../hooks/toast';

interface ToastProps {
  message: ToastMessage;
  style: object;
}

const icons = {
  info: <FiInfo size={24} />,
  error: <FiAlertCircle size={24} />,
  success: <FiCheckCircle size={24} />,
};

const Toast: React.FC<ToastProps> = ({ message, style }) => {
  const { removeToast } = useToast();
  const status = message.type || 'info';
  const statusList = {
    success: {
      color: 'text-green-500',
    },
    error: {
      color: 'text-red-500',
    },
    info: {
      color: 'text-blue-500',
    },
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      removeToast(message.id);
    }, 3000);

    // O retorno de um useEffect é usado sempre que o componente
    // deixa de existir. Algo como o ngOnDestroy.
    return () => {
      clearTimeout(timer);
    };
  }, [removeToast, message.id]);

  return (
    // <div type={message.type} hasDescription={!!message.description} style={style}>
    <div className="fixed bottom-5 right-5">
      <div
        className="max-w-xs bg-white border rounded-md shadow-lg dark:bg-slate-800 dark:border-slate-700"
        role="alert"
      >
        <div className="flex p-4">
          <div className={`${statusList[status].color}  flex-shrink-0`}>
            {icons[status]}
          </div>

          <div className="ml-4">
            {message.description && (
              <>
                <h3 className="text-slate-800  font-semibold dark:text-white">
                  <span>{message.title}</span>
                </h3>

                <div className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                  {message.description && <>{message.description}</>}
                </div>
              </>
            )}

            {!message.description && (
              <p className="text-sm text-gray-700 dark:text-gray-400">
                <span>{message.title}</span>
              </p>
            )}

            {/* <div className="mt-4">
              <div className="flex space-x-3">
                <button
                  type="button"
                  onClick={() => removeToast(message.id)}
                  className="inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-medium text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm"
                >
                  Close
                </button>
              </div>
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Toast;
