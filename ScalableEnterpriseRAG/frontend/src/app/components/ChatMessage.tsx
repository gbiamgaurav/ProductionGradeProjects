import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  timestamp: string;
}

export function ChatMessage({ message, isBot, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 ${isBot ? 'justify-start' : 'justify-end'}`}>
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      <div className="flex flex-col gap-1 max-w-[70%]">
        <div
          className={`rounded-2xl px-4 py-2.5 ${
            isBot
              ? 'bg-gray-100 text-gray-900 rounded-tl-sm'
              : 'bg-blue-500 text-white rounded-tr-sm'
          }`}
        >
          <p className="text-sm leading-relaxed">{message}</p>
        </div>
        <span className={`text-xs text-gray-500 px-2 ${!isBot && 'text-right'}`}>
          {timestamp}
        </span>
      </div>

      {!isBot && (
        <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center flex-shrink-0">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
}
