import './../css/app.css';
import { createRoot } from 'react-dom/client';
import { useState, useRef, useEffect } from 'react';

function App() {
  const [messages, setMessages] = useState([
    { role: 'ai', text: 'Assalamu\'alaikum. Saya Asisten Mufti Maktabah Syamilah AI. Apa yang ingin Anda tanyakan seputar hukum fikih hari ini?', sources: null }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setMessages((prev) => [...prev, { role: 'user', text: userMessage, sources: null }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat-mufti', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ pertanyaan: userMessage })
      });

      const data = await response.json();

      if (response.ok) {
        setMessages((prev) => [...prev, {
          role: 'ai',
          text: data.jawaban_ai,
          sources: { arab: data.referensi_arab, kitab: data.sumber_kitab }
        }]);
      } else {
        setMessages((prev) => [...prev, { role: 'ai', text: `Maaf, terjadi kesalahan: ${data.message}` }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'ai', text: 'Maaf, gagal terhubung ke server AI.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans selection:bg-amber-200 selection:text-slate-900">

      {/* Header Premium - Glassmorphism */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 py-4 px-6 flex items-center justify-between sticky top-0 z-20">
        <div className="flex items-center gap-4 max-w-4xl mx-auto w-full">
          {/* Logo Icon Premium */}
          <div className="w-12 h-12 bg-gradient-to-br from-slate-800 to-slate-950 rounded-2xl flex items-center justify-center text-amber-400 font-serif font-bold text-2xl shadow-lg border border-slate-700/50">
            M
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Mufti <span className="text-amber-600">AI</span></h1>
            <p className="text-sm text-slate-500 font-medium">Powered by Maktabah Syamilah</p>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-8 w-full max-w-4xl mx-auto flex flex-col gap-6 scroll-smooth">
        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in fade-in slide-in-from-bottom-2 duration-300`}>

            {/* Avatar AI (Opsional, hanya muncul untuk AI) */}
            {msg.role === 'ai' && (
              <div className="w-8 h-8 rounded-full bg-slate-900 flex items-center justify-center text-amber-400 text-xs font-bold mr-3 mt-1 flex-shrink-0 shadow-sm">
                AI
              </div>
            )}

            <div className={`max-w-[85%] sm:max-w-[75%] px-6 py-4 shadow-sm ${
              msg.role === 'user'
                ? 'bg-slate-900 text-white rounded-3xl rounded-tr-sm font-medium' // Gaya User: Deep Slate
                : 'bg-white border border-slate-200/60 text-slate-800 rounded-3xl rounded-tl-sm' // Gaya AI: Putih Bersih
            }`}>
              <p className="whitespace-pre-wrap leading-relaxed text-[15px] sm:text-base">{msg.text}</p>

              {/* Box Sumber Referensi Premium */}
              {/* Box Sumber Referensi Premium */}
{msg.sources && msg.sources.kitab && msg.sources.arab && (
  <div className="mt-5 pt-5 border-t border-slate-100">
    <div className="flex items-center gap-2 mb-3">
      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0-3.332.477-4.5 1.253" />
      </svg>
      <p className="text-xs font-bold text-amber-600 uppercase tracking-widest">{msg.sources.kitab}</p>
    </div>
    {/* Teks Arab dengan Border Kanan (RTL) */}
    <div className="bg-slate-50/80 border-r-4 border-amber-400 p-4 rounded-xl rounded-tr-sm border border-slate-100/80 shadow-inner">
      <p className="text-lg leading-loose text-slate-800 font-arabic text-right" dir="rtl">
        {msg.sources.arab}
      </p>
    </div>
  </div>
)}
            </div>
          </div>
        ))}

        {/* Indikator Loading Elegan */}
        {isLoading && (
          <div className="flex justify-start items-start animate-in fade-in duration-300">
            <div className="w-8 h-8 rounded-full bg-slate-900 flex items-center justify-center text-amber-400 text-xs font-bold mr-3 mt-1 flex-shrink-0 shadow-sm">
              AI
            </div>
            <div className="bg-white border border-slate-200/60 rounded-3xl rounded-tl-sm px-6 py-5 shadow-sm flex gap-2.5 items-center">
              <span className="animate-bounce w-2 h-2 bg-slate-300 rounded-full"></span>
              <span className="animate-bounce w-2 h-2 bg-slate-400 rounded-full" style={{ animationDelay: '0.15s' }}></span>
              <span className="animate-bounce w-2 h-2 bg-slate-500 rounded-full" style={{ animationDelay: '0.3s' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area Floating Style */}
      <footer className="bg-slate-50/80 backdrop-blur-md p-4 sm:p-6 pb-6 sm:pb-8 z-10">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto flex gap-3 relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ketik pertanyaan fikih Anda di sini..."
            className="flex-1 bg-white border border-slate-200 shadow-sm rounded-full px-6 py-4 focus:outline-none focus:ring-4 focus:ring-slate-100 focus:border-slate-400 text-slate-800 transition-all text-[15px]"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-slate-900 text-white rounded-full w-14 h-14 flex items-center justify-center hover:bg-slate-800 hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-none flex-shrink-0 group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5 ml-1 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform">
              <path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" />
            </svg>
          </button>
        </form>
      </footer>
    </div>
  );
}

const container = document.getElementById('root');
if (container) {
    const root = createRoot(container);
    root.render(<App />);
}

export default App;
