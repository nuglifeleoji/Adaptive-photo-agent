import React, { useRef, useState } from "react";
import Webcam from "react-webcam";

const COUNTDOWN = ["3", "2", "1", "茄子"];

export default function PhotoAgentDemo() {
  const webcamRef = useRef(null);
  const [aiSuggestion, setAiSuggestion] = useState("请调整姿势，准备拍照");
  const [countdown, setCountdown] = useState("");
  const [photo, setPhoto] = useState(null);
  const [isCounting, setIsCounting] = useState(false);

  // 语音播报
  const speak = (text) => {
    const synth = window.speechSynthesis;
    if (synth.speaking) synth.cancel();
    const utter = new window.SpeechSynthesisUtterance(text);
    utter.lang = "zh-CN";
    synth.speak(utter);
  };

  // 拍照倒计时
  const handleTakePhoto = async () => {
    setIsCounting(true);
    for (let i = 0; i < COUNTDOWN.length; i++) {
      setCountdown(COUNTDOWN[i]);
      speak(COUNTDOWN[i]);
      // eslint-disable-next-line no-await-in-loop
      await new Promise((res) => setTimeout(res, 700));
    }
    setCountdown("");
    // 拍照
    const imageSrc = webcamRef.current.getScreenshot();
    // 上传到后端
    fetch('http://localhost:5000/take_photo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ img_b64: imageSrc })
    })
      .then(res => res.json())
      .then(data => {
        setPhoto(`http://localhost:5000${data.photo_url}`);
        speak("照片已拍摄完成");
        setIsCounting(false);
        setAiSuggestion("如需再来一张，请点击按钮或说“再来一张”");
      });
  };

  // 语音输入（Web Speech API）
  const handleVoiceInput = () => {
    const recognition = new window.webkitSpeechRecognition() || new window.SpeechRecognition();
    recognition.lang = "zh-CN";
    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      // 发送到后端获取AI建议
      fetch('http://localhost:5000/ai_suggestion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_text: text })
      })
        .then(res => res.json())
        .then(data => {
          setAiSuggestion(data.ai_reply);
          speak(data.ai_reply);
          if (text.includes("再来一张")) {
            setPhoto(null);
            setAiSuggestion("请调整姿势，准备拍照");
          }
        });
    };
    recognition.start();
  };

  const handleUpload = (files) => {
    const formData = new FormData();
    for (let file of files) {
      formData.append('photos', file);
    }
    fetch('http://localhost:5000/upload_user_style', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        alert('风格分析完成！');
        // 可显示风格标签
      });
  };

  return (
    <div style={{ maxWidth: 480, margin: "0 auto", textAlign: "center" }}>
      <h2>智能拍照助手演示</h2>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={400}
        videoConstraints={{ facingMode: "user" }}
        style={{ borderRadius: 8, marginBottom: 12 }}
      />
      <div style={{ fontSize: 24, color: "#1890ff", minHeight: 32 }}>
        {countdown || aiSuggestion}
      </div>
      <div style={{ margin: "16px 0" }}>
        <button onClick={handleTakePhoto} disabled={isCounting || !!photo}>
          拍照
        </button>
        <button onClick={handleVoiceInput} style={{ marginLeft: 12 }}>
          语音输入
        </button>
        {photo && (
          <button
            onClick={() => {
              setPhoto(null);
              setAiSuggestion("请调整姿势，准备拍照");
            }}
            style={{ marginLeft: 12 }}
          >
            再来一张
          </button>
        )}
      </div>
      {photo && (
        <div>
          <img src={photo} alt="拍照结果" style={{ width: 320, borderRadius: 8 }} />
          <div style={{ marginTop: 8 }}>
            <a href={photo} download="photo.jpg">
              下载照片
            </a>
          </div>
        </div>
      )}
    </div>
  );
}