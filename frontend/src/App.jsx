import './App.css';
import React,{useState} from 'react';
import axios from "axios"

function App() {
  const [input,setInput] = useState("");
  const [targetLang,setTargetLang] = useState("fr");
  const[messages,setMessages] = useState(["BabelMate 😏: Hello! I’m your translation companion — ready to help! ✨"]);
  const [languageLabel,setLanguageLabel] = useState("");

  const languageMap = {
    fr : 'French',
    de: 'German',
    hi: 'Hindi',
    es: 'Spanish',
    zh: 'Chinese',
    ar: 'Arabic',
    jap: 'Japanese',
    vi: 'Vietnamese',

  }

  const handleTranslate = async() =>{
    if(!input.trim()) return;

    const userMessage = `You 🥰: ${input}`;
    setMessages((prev) => [...prev,userMessage])
    try{
      const res =  await axios.post("http://localhost:8000/translate",{
        text: input,
        target_lang: targetLang,
        model: "huggingface",
      });
      const langLabel = languageMap[targetLang];
      setLanguageLabel(langLabel);
      const translatedText = res.data.translated_text;
      const botMessage = `BabelMate 😏 [Translated to ${langLabel}] : ${translatedText}`
      setMessages((prev) => [...prev, botMessage]);
    }catch(error){
      setMessages((prev) => [...prev,"BabelMate 😏: Failed To Translate."])
    }

    setInput("")
  };

  return (
    <div className='app-container'>
      <h2 className='heading'>BabelMate : A Translator Chatbot</h2>
       <div className='chat-window'>
        {messages.map((msg,idx) => (
          <p key = {idx} className={msg.startsWith("You") ? "user-msg" :"bot-msg"}>
            {msg}
          </p>
        ))}
       </div>
       <div className='controls'>
        <input type='text' value={input} placeholder='Type your Message...' onChange={(e) => setInput(e.target.value)} />
        <select value={targetLang} onChange={(e) =>setTargetLang(e.target.value)}>
        <option value="fr">French</option>
        <option value="de">German</option>
        <option value="es">Spanish</option>
        {/* <option value="ta">Tamil</option> */}
        <option value="hi">Hindi</option>
        <option value="zh">Chinese</option>
        <option value="ar">Arabic</option>
        <option value="jap">Japanese</option>
        <option value="vi">Vietnamese</option>
      </select>
      <button onClick={handleTranslate}>Translate</button>
     </div>
    </div>
  );

}

export default App;
