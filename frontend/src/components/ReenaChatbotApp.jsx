//working output formate 
// import React, { useState } from "react";
// import axios from "axios";

// const ReenaChatbotApp = () => {
//   const [messages, setMessages] = useState([
//     { sender: "bot", text: "👋 Hello! I’m Reena, your insurance assistant. How can I help you today?" }
//   ]);
//   const [userInput, setUserInput] = useState("");
//   const [loading, setLoading] = useState(false);

//   const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

//   const displayBotMessageStepByStep = async (fullMessage) => {
//     const sentences = fullMessage.split(/(?<=[.?!])\s+/); // Split by sentence

//     for (const sentence of sentences) {
//       setMessages((prev) => [...prev, { sender: "bot", text: sentence }]);
//       await delay(1200); // 1.2 sec delay between each part
//     }
//   };

//   const sendMessage = async () => {
//     if (!userInput.trim()) return;

//     const newMessages = [...messages, { sender: "user", text: userInput }];
//     setMessages(newMessages);
//     setUserInput("");
//     setLoading(true);

//     try {
//       const response = await axios.post("http://localhost:5000/chat", {
//         message: userInput
//       });

//       const botReply = response.data.response || "⚠️ No response from bot.";
//       await displayBotMessageStepByStep(botReply);
//     } catch (error) {
//       setMessages((prev) => [
//         ...prev,
//         { sender: "bot", text: "❌ Sorry, something went wrong connecting to Reena's brain!" }
//       ]);
//       console.error("Error from backend:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleKeyPress = (e) => {
//     if (e.key === "Enter") {
//       sendMessage();
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
//       <div className="w-full max-w-xl bg-white rounded-lg shadow-md p-6">
//         <h1 className="text-2xl font-bold mb-4 text-purple-700">Reena 🤖 – Insurance Assistant</h1>

//         <div className="overflow-y-auto h-96 border border-gray-200 rounded-md p-3 mb-4 bg-gray-50">
//           {messages.map((msg, idx) => (
//             <div
//               key={idx}
//               className={`mb-2 p-2 rounded-md text-sm ${
//                 msg.sender === "bot"
//                   ? "bg-purple-100 text-purple-800 self-start"
//                   : "bg-blue-100 text-blue-800 self-end text-right"
//               }`}
//             >
//               {msg.text}
//             </div>
//           ))}
//           {loading && <div className="text-sm text-gray-500">Reena is typing...</div>}
//         </div>

//         <div className="flex gap-2">
//           <input
//             type="text"
//             className="flex-grow p-2 border rounded-md"
//             placeholder="Type your message..."
//             value={userInput}
//             onChange={(e) => setUserInput(e.target.value)}
//             onKeyPress={handleKeyPress}
//           />
//           <button
//             onClick={sendMessage}
//             className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md"
//             disabled={loading}
//           >
//             Send
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };



// export default ReenaChatbotApp;

// #with auto croll
// import React, { useState, useRef, useEffect } from "react";
// import axios from "axios";
// import ReactMarkdown from "react-markdown";

// const ReenaChatbotApp = () => {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(false);
//   const messagesEndRef = useRef(null); // ✅ Auto-scroll ref

//   // ✅ Scroll to bottom when messages update
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     const userMessage = { sender: "user", text: input };
//     setMessages((prev) => [...prev, userMessage]);
//     setInput("");
//     setLoading(true);

//     try {
//       const res = await axios.post("/chat", { message: input });
//       const botReply = res.data.response;

//       setMessages((prev) => [...prev, { sender: "bot", text: botReply }]);
//     } catch (err) {
//       console.error("❌ Error sending message:", err);
//       setMessages((prev) => [
//         ...prev,
//         { sender: "bot", text: "Sorry, something went wrong." },
//       ]);
//     }

//     setLoading(false);
//   };

//   return (
//     <div className="max-w-3xl mx-auto p-4">
//       <h1 className="text-3xl font-bold mb-4 text-center text-blue-700">💬 Reena Insurance Chatbot</h1>

//       <div className="bg-white rounded-xl p-4 shadow-md h-[60vh] overflow-y-auto space-y-4">
//         {messages.map((msg, idx) => (
//           <div
//             key={idx}
//             className={`whitespace-pre-wrap p-3 rounded-lg ${
//               msg.sender === "user"
//                 ? "bg-blue-100 text-right ml-auto max-w-[75%]"
//                 : "bg-gray-100 text-left mr-auto max-w-[75%]"
//             }`}
//           >
//             <ReactMarkdown>{msg.text}</ReactMarkdown>
//           </div>
//         ))}
//         {loading && (
//           <div className="text-gray-500 italic text-sm">Reena is typing...</div>
//         )}
//         <div ref={messagesEndRef} /> {/* ✅ Scroll target */}
//       </div>

//       <div className="mt-4 flex gap-2">
//         <input
//           type="text"
//           className="flex-1 p-2 border rounded"
//           placeholder="Type your message..."
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={(e) => e.key === "Enter" && sendMessage()}
//         />
//         <button
//           className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
//           onClick={sendMessage}
//         >
//           Send
//         </button>
//       </div>
//     </div>
//   );
// };

// export default ReenaChatbotApp;


//full screen
import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const ReenaChatbotApp = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null); // ✅ Auto-scroll ref

  // ✅ Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("/chat", { message: input });
      const botReply = res.data.response;

      setMessages((prev) => [...prev, { sender: "bot", text: botReply }]);
    } catch (err) {
      console.error("❌ Error sending message:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, something went wrong." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-gray-100">
      <header className="text-3xl font-bold py-4 text-center text-blue-700 bg-white shadow">
        💬 AIVA Life Insurance Specialist
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`whitespace-pre-wrap p-3 rounded-lg max-w-[75%] ${
              msg.sender === "user"
                ? "bg-blue-100 text-right ml-auto"
                : "bg-gray-100 text-left mr-auto"
            }`}
          >
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        ))}
        {loading && (
          <div className="text-gray-500 italic text-sm">AIVA is typing...</div>
        )}
        <div ref={messagesEndRef} /> {/* ✅ Scroll target */}
      </main>

      <footer className="flex p-4 bg-white border-t gap-2">
        <input
          type="text"
          className="flex-1 p-2 border rounded"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          onClick={sendMessage}
        >
          Send
        </button>
      </footer>
    </div>
  );
};

export default ReenaChatbotApp;
