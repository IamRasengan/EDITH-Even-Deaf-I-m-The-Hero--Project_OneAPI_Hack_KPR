import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';

function App() {
  const [prediction, setPrediction] = useState("");
  const webcamRef = useRef(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  // Function to capture and send frames
  const captureAndSendFrame = useCallback(async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    // Send the captured image frame to the Flask backend
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: imageSrc })
    });
    
    const data = await response.json();
    setPrediction(data.predictions); // Assuming your Flask returns 'predictions'
  }, [webcamRef]);

  return (
    <div>
      <h1>Gesture Recognition</h1>
      <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
      />
      <button onClick={captureAndSendFrame}>Capture and Predict</button>
      <h2>Prediction: {prediction}</h2>
    </div>
  );
}

export default App;
