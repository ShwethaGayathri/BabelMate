import './App.css';
import React,{useState} from 'react';
import axios from "axios"

function App() {
  const [text,setText] = useState("");
  const [targetLang,setTargetLang] = useState("");
  const[translated,setTranslated] = useState("");

  const handleTranslate = async() =>{
    try{
      const res =  await axios.post("http://localhost:8000/translate",{
        text,
        target_lang: targetLang,
        model: "huggingface",
      });
      setTranslated(res.data.translated_text);
    }catch(error){
      console.error(error);
    }
  };

  return (
    <div className='app'>
      <h2>BabelMate : A Translator Chatbot</h2>
      <textarea 
      placeholder='Enter Text'
      value= {text}
      onChange={(e) => setText(e.target.value)}
      />
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
      <div className='output'>
        <strong>Translation:</strong> {translated}
      </div>
    </div>
  );

}

export default App;
