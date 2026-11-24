import { useState, useCallback, useRef, useEffect } from "react";

export function useVoice(onResult: (text: string) => void) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SR) {
      setSupported(true);
      const rec = new SR();
      rec.lang = "es-ES";
      rec.interimResults = false;
      rec.onresult = (e: any) => {
        const text = e.results[0][0].transcript;
        onResult(text);
      };
      rec.onend = () => setListening(false);
      rec.onerror = () => setListening(false);
      recognitionRef.current = rec;
    }
  }, [onResult]);

  const start = useCallback(() => {
    if (recognitionRef.current && !listening) {
      setListening(true);
      recognitionRef.current.start();
    }
  }, [listening]);

  const stop = useCallback(() => {
    if (recognitionRef.current && listening) {
      recognitionRef.current.stop();
      setListening(false);
    }
  }, [listening]);

  const speak = useCallback((text: string) => {
    if ("speechSynthesis" in window) {
      const u = new SpeechSynthesisUtterance(text);
      u.lang = "es-ES";
      window.speechSynthesis.speak(u);
    }
  }, []);

  return { listening, supported, start, stop, speak };
}