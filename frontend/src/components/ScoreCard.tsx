import React from 'react';

interface ScoreCardProps {
  title: string;
  score: number;
  maxScore: number | null;
  color: 'green' | 'yellow' | 'red' | 'blue';
  icon: React.ReactNode;
  description: string;
  details?: Array<{ label: string; value: number | string }>;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  title,
  score,
  maxScore,
  color,
  icon,
  description,
  details = []
}) => {
  const colorClasses = {
    green: 'bg-green-50 border-green-200 text-green-800',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    red: 'bg-red-50 border-red-200 text-red-800',
    blue: 'bg-blue-50 border-blue-200 text-blue-800'
  };

  const iconColorClasses = {
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    red: 'text-red-600',
    blue: 'text-blue-600'
  };

  return (
    <div className={`p-6 rounded-lg border-2 ${colorClasses[color]}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">{title}</h3>
        <div className={iconColorClasses[color]}>
          {icon}
        </div>
      </div>
      
      <div className="mb-2">
        <span className="text-3xl font-bold">
          {score}
          {maxScore && <span className="text-lg font-normal">/{maxScore}</span>}
        </span>
      </div>
      
      <p className="text-sm mb-4">{description}</p>
      
      {details.length > 0 && (
        <div className="space-y-2">
          {details.map((detail, index) => (
            <div key={index} className="flex justify-between text-sm">
              <span>{detail.label}:</span>
              <span className="font-medium">{detail.value}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};