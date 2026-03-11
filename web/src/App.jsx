import React, { useEffect, useRef, useState } from 'react';
import { Hands } from '@mediapipe/hands';
import * as cam from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import { HAND_CONNECTIONS } from '@mediapipe/hands';
import { detectGesture } from './utils/GestureLogic';
import { Trash2, Volume2, VolumeX, Sparkles, MessageSquare } from 'lucide-react';
import confetti from 'canvas-confetti';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [currentSign, setCurrentSign] = useState("WAITING...");
  const [history, setHistory] = useState([]);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const lastSignRef = useRef("");
  const signCounterRef = useRef(0);

  const speak = (text) => {
    if ('speechSynthesis' in window && voiceEnabled) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    }
  };

  const getMLPrediction = async (landmarks) => {
    const flatLandmarks = landmarks.flatMap(lm => [lm.x, lm.y]);
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ landmarks: flatLandmarks }),
      });
      const data = await response.json();
      return data.prediction || "UNKNOWN";
    } catch (e) {
      return "UNKNOWN";
    }
  };

  const addToHistory = (word) => {
    setHistory(prev => {
      if (prev.length > 0 && prev[prev.length - 1] === word) return prev;
      return [...prev, word];
    });
  };

  const clearHistory = () => setHistory([]);

  const triggerConfetti = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#00d2ff', '#9d50bb', '#ffffff']
    });
  };

  const [stabilityPerc, setStabilityPerc] = useState(0);
  const THRESHOLD = 12; // Wait for 12 frames of same sign

  useEffect(() => {
    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.7, // Increased for accuracy
      minTrackingConfidence: 0.7,
    });

    hands.onResults(async (results) => {
      const canvasCtx = canvasRef.current.getContext('2d');
      if (!canvasCtx || !canvasRef.current) return;

      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];

        drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: '#00d2ff', lineWidth: 4 });
        drawLandmarks(canvasCtx, landmarks, {
          color: '#ffffff',
          lineWidth: 2,
          radius: (data) => data.from ? 4 : 2
        });

        let gesture = detectGesture(landmarks);

        if (gesture === "UNKNOWN") {
          gesture = await getMLPrediction(landmarks);
        }

        setCurrentSign(gesture);

        if (gesture !== "UNKNOWN" && gesture !== "NONE") {
          if (gesture === lastSignRef.current) {
            signCounterRef.current += 1;
            setStabilityPerc((signCounterRef.current / THRESHOLD) * 100);

            if (signCounterRef.current === THRESHOLD) {
              addToHistory(gesture);
              triggerConfetti();
              speak(gesture);
            }
          } else {
            lastSignRef.current = gesture;
            signCounterRef.current = 1;
            setStabilityPerc(0);
          }
        }
      } else {
        setCurrentSign("NONE");
        setStabilityPerc(0);
        if (signCounterRef.current > 0) signCounterRef.current -= 0.5;
      }
      canvasCtx.restore();
    });

    if (videoRef.current) {
      const camera = new cam.Camera(videoRef.current, {
        onFrame: async () => {
          if (videoRef.current) await hands.send({ image: videoRef.current });
        },
        width: 1280,
        height: 720,
      });
      camera.start();
    }

    return () => {
      hands.close();
    };
  }, [voiceEnabled]);

  return (
    <div className="app-container">
      <header>
        <div className="logo-container">
          <Sparkles color="#00d2ff" size={32} />
          <h1>SignSpeak AI</h1>
        </div>
        <div className="status-label" style={{ margin: 0, alignSelf: 'center', opacity: 0.7 }}>
          PREMIUM v2.5
        </div>
      </header>

      <main className="main-grid">
        <section className="camera-section">
          <video ref={videoRef} className="video-feed" playsInline muted />
          <canvas ref={canvasRef} className="canvas-overlay" width="1280" height="720" />
          <div className="scanning-indicator">
            <div className="dot"></div>
            NEURAL ENGINE ACTIVE
          </div>
        </section>

        <section className="info-section">
          <div className="status-card">
            <div className="status-label">Live Detection</div>
            <div className="status-value">{currentSign}</div>
            {currentSign !== "NONE" && currentSign !== "UNKNOWN" && (
              <div className="stability-container">
                <div className="stability-bar" style={{ width: `${Math.min(stabilityPerc, 100)}%` }}></div>
              </div>
            )}
          </div>

          <div className="history-card">
            <div className="status-label" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <MessageSquare size={16} /> Translation Stream
            </div>
            <div className="history-list">
              {history.length === 0 ? (
                <span className="empty-state">Ready to translate...</span>
              ) : (
                history.map((word, i) => (
                  <span key={i} className="history-word">{word}</span>
                ))
              )}
            </div>
          </div>

          <div className="controls-card">
            <button
              className={`btn ${voiceEnabled ? 'btn-primary' : ''}`}
              onClick={() => setVoiceEnabled(!voiceEnabled)}
            >
              {voiceEnabled ? <Volume2 size={20} /> : <VolumeX size={20} />}
              {voiceEnabled ? "Voice ON" : "Voice OFF"}
            </button>
            <button className="btn" onClick={clearHistory}>
              <Trash2 size={20} />
              Reset
            </button>
          </div>
        </section>
      </main>

      <footer>
        &copy; 2026 SignSpeak Pro | Real-time Edge Intelligence
      </footer>
    </div>
  );
}

export default App;
