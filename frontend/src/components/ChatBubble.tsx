import { ChatMessage } from "@/store/chatStore";
import { User, Bot } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatBubbleProps {
  message: ChatMessage;
}

const ChatBubble = ({ message }: ChatBubbleProps) => {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex gap-3 mb-4 animate-fadeInSlide",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
          isUser ? "bg-primary" : "bg-accent"
        )}
      >
        {isUser ? (
          <User className="w-5 h-5 text-primary-foreground" />
        ) : (
          <Bot className="w-5 h-5 text-accent-foreground" />
        )}
      </div>

      {/* Message bubble */}
      <div
        className={cn(
          "flex flex-col max-w-[80%]",
          isUser ? "items-end" : "items-start"
        )}
      >
        <div
          className={cn(
            "rounded-2xl px-4 py-3 shadow-md break-words overflow-hidden",
            isUser
              ? "bg-primary text-primary-foreground rounded-tr-sm"
              : "bg-card text-card-foreground border border-border rounded-tl-sm"
          )}
        >
          {/* Image */}
          {message.imageUrl && (
            <img
              src={message.imageUrl}
              alt="Uploaded"
              className="max-w-full h-auto rounded-lg mb-2 border border-border"
            />
          )}

          {/* Markdown Content */}
          {message.content && (
            <div
              className={cn(
                "prose prose-sm max-w-none leading-relaxed",
                // Inverse prose colors for user bubble (primary bg)
                isUser
                  ? "prose-invert text-primary-foreground"
                  : "dark:prose-invert text-card-foreground"
              )}
            >
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  // Override link behavior to open in new tab
                  a: ({ node, ...props }) => (
                    <a {...props} target="_blank" rel="noopener noreferrer" className="underline font-medium" />
                  ),
                  // Style paragraphs
                  p: ({ node, ...props }) => (
                     <p {...props} className="mb-2 last:mb-0" />
                  ),
                  // Style lists
                  ul: ({ node, ...props }) => (
                    <ul {...props} className="list-disc pl-4 mb-2" />
                  ),
                  ol: ({ node, ...props }) => (
                    <ol {...props} className="list-decimal pl-4 mb-2" />
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}

          {/* Agent tag (assistant messages only) */}
          {message.agent && (
            <div className="text-xs mt-2 opacity-60 pt-2 border-t border-border/20">
              Agent: {message.agent}
            </div>
          )}
        </div>

        {/* Timestamp */}
        <div
          className={cn(
            "text-xs text-muted-foreground mt-1",
            isUser ? "text-right" : "text-left"
          )}
        >
          {format(new Date(message.timestamp), "HH:mm")}
        </div>
      </div>
    </div>
  );
};

export default ChatBubble;
