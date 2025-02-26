import React, { useEffect, useRef, useState } from "react";
import { Container, Button, Form, Alert, Row, Col } from "react-bootstrap";
import jsQR from "jsqr";
import { sendPointsToVendor } from "../../api/user";

import "../../styles/UserSendPoints.css";

const UserSendPoints = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [scanResult, setScanResult] = useState(null);
  const [points, setPoints] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isCameraSupported, setIsCameraSupported] = useState(true);

  // Start video stream
  useEffect(() => {
    let stream = null;

    const startVideo = async () => {
      try {
        const constraints = {
          video: {
            facingMode: "environment",
            width: { ideal: 1280 },
            height: { ideal: 720 },
          },
        };
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play().catch((error) => {
              console.error("Error playing video:", error);
            });
          };
        }
      } catch (error) {
        console.error("Error accessing video stream:", error);
        setIsCameraSupported(false);
      }
    };

    if (isScanning) {
      startVideo();
    } else if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
    }

    return () => {
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [isScanning]);

  // QR Code Scanning Logic
  useEffect(() => {
    const scanQRCode = () => {
      if (!videoRef.current || !canvasRef.current) return;

      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");

      if (video.videoWidth === 0 || video.videoHeight === 0) {
        return;
      }

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
      const code = jsQR(imageData.data, imageData.width, imageData.height);

      if (code) {
        const vendorDetails = code.data.split(": ")[1]; // Adjust this based on your QR code format
        console.log("Vendor Details:", vendorDetails);
        setScanResult(vendorDetails);
        if (video.srcObject) {
          const tracks = video.srcObject.getTracks();
          tracks.forEach((track) => track.stop());
        }

        setIsScanning(false);
      }
    };

    if (isScanning) {
      const interval = setInterval(scanQRCode, 500); // Continuously scan every 500ms
      return () => clearInterval(interval);
    }
  }, [isScanning]);

  // Form submission to send points to the vendor
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(null); // Reset error message on form submission

    if (points && scanResult) {
      try {
        // Call the API to send points to the vendor
        const response = await sendPointsToVendor(scanResult, points); // Pass vendor_id (scanResult) and points

        if (response) {
          console.log("Response from backend:", response);
          alert("Points sent successfully!");
        } else {
          setErrorMessage("Invalid response from the server");
        }
      } catch (error) {
        setErrorMessage(error.message || "Error sending points.");
      }
    } else {
      setErrorMessage("Please scan a valid QR code and enter a valid amount.");
    }
  };

  return (
    <>
      {/* Container with responsive layout */}
      <Container fluid className="scanner-page text-center pt-5 pb-5">
        <Row className="justify-content-center">
          <Col xs={12} md={8}>
            <p>
              <b style={{color:"#015295"}}>ScanQRCodetoPay</b>
            </p>

            {isCameraSupported ? (
              <>
                {!scanResult ? (
                  <div>
                    <video
                      ref={videoRef}
                      className="border rounded"
                      style={{ width: "100%", maxWidth: "500px" }}
                      playsInline
                    />
                    <div className="text-center">
                      <img
                        src={
                          isScanning
                            ? "https://cdn-icons-png.flaticon.com/128/18357/18357620.png"
                            : "https://cdn-icons-png.flaticon.com/128/18357/18357620.png"
                        } // Change icons according to the state
                        alt={isScanning ? "Stop Scan" : "Start Scan"}
                        className="cursor-pointer"
                        onClick={() => setIsScanning(!isScanning)} // Toggle scanning state
                        style={{ width: "50px", height: "50px" }} // Adjust the icon size
                      />
                      <div>
                        <span className="fw-bold" style={{color:"#015295"}}> 
                          {isScanning ? "Stop Scan" : "Start Scan"}
                        </span>
                      </div>
                    </div>
                    {/* </div> */}
                  </div>
                ) : (
                  <div>
                    <p>
                      <strong>Vendor Scanned:</strong> {scanResult}
                    </p>
                    <Form onSubmit={handleSubmit}>
                      <Form.Group>
                        <Form.Label>Enter Points</Form.Label>
                        <Form.Control
                          type="number"
                          value={points}
                          onChange={(e) => setPoints(e.target.value)}
                          placeholder="Enter points"
                          required
                          min="1"
                        />
                      </Form.Group>
                      <Button type="submit" className="mt-3" variant="primary">
                        Send Points
                      </Button>
                    </Form>
                  </div>
                )}

                {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
              </>
            ) : (
              <Alert variant="danger">
                Camera access is not supported on this device. Please try again
                with a device that has a camera.
              </Alert>
            )}
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default UserSendPoints;
