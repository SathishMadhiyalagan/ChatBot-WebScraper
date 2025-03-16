import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Loader2 } from "lucide-react";

const API_URL = "http://127.0.0.1:8000/api/query";

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
}

const Chat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(API_URL, {
        user_id: 1,
        query: input,
      });

      const botMessage: Message = {
        id: messages.length + 2,
        text: response.data.answer || "No response from bot",
        sender: "bot",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: messages.length + 2,
          text: "❌ Error: Failed to fetch response.",
          sender: "bot",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto p-6 bg-white rounded-lg shadow-lg border">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">AI Chat</h2>

      {/* Chat Display */}
      <div className="h-96 overflow-y-auto p-3 bg-gray-100 rounded border space-y-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`p-3 max-w-[75%] text-sm rounded-lg ${msg.sender === "user"
                ? "bg-blue-500 text-white ml-auto self-end"
                : "bg-gray-300 text-black mr-auto self-start"
              }`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input Box */}
      <div className="flex mt-4 border rounded-lg overflow-hidden">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-3 border-none outline-none"
          placeholder="Type a message..."
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-5 bg-blue-500 text-white flex items-center justify-center transition hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? <Loader2 className="animate-spin" /> : <Send />}
        </button>
      </div>
    </div>
  );
};

export default Chat;
