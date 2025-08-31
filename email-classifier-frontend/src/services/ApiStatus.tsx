import React from 'react';
import { useApiStatus } from '../services/api';

const ApiStatus: React.FC = () => {
  const { isOnline, isChecking } = useApiStatus();

  if (isChecking) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-600">
        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
        Verificando API...
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
      <span className={isOnline ? 'text-green-600' : 'text-red-600'}>
        {isOnline ? 'API Online' : 'API Offline'}
      </span>
    </div>
  );
};

export default ApiStatus;
