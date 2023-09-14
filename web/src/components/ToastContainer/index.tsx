import React from 'react';
import { useTransition, animated } from '@react-spring/web';

import Toast from './Toast';

import { ToastMessage } from '../../hooks/toast';

interface ToastContainerProps {
  messages: ToastMessage[];
}

const ToastComponent: React.FC<ToastContainerProps> = ({ messages }) => {
  const transitions = useTransition(messages, {
    from: { right: '-120%', opacity: 0 },
    enter: { right: '0%', opacity: 1 },
    leave: { right: '-120%', opacity: 1 },
  });

  return (
    <div>
      {transitions((style, item) => (
        <Toast style={style} message={item} />
      ))}
    </div>
  );
};

export default ToastComponent;
