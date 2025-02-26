import React, { useEffect, useState } from 'react';
import { Alert, Button, Container, Spinner } from 'react-bootstrap';
import { fetchVendorQRCode } from '../../api/vendor'; 
import Footer from '../common/Footer';

const VendorScannerScreen = () => {
  const [qrCodeData, setQrCodeData] = useState(null); 
  const [loading, setLoading] = useState(false); 
  const [error, setError] = useState(''); 
  const[vendorName,setVendorName]=useState(null);

  useEffect(() => {
    const getQRCode = async () => {
      setLoading(true);
      try {
        const qrCode = await fetchVendorQRCode(); 
        console.log('QR Code (Base64):', qrCode.data.vendor); 
        console.log('QR Code Data Length:', qrCode.length); 

        setQrCodeData(qrCode.data.vendor.qr_code); 
        setVendorName(qrCode.data.vendor.vendor_name);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching QR Code:', err);
        setError('Error fetching QR Code.');
        setLoading(false);
      }
    };

    getQRCode(); 
  }, []);

  const downloadQRCode = () => {
    if (!qrCodeData) return;
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${qrCodeData}`;
    link.download = 'vendor_qr_code.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <>
      <Container fluid className="vendor-scanner text-center pt-5 pb-5" style={{ marginTop: '80px', marginBottom: '20px' }}>
        <h4 style={{ color: '#015295' }}>QR Code</h4>
        {vendorName &&  <h3 style={{color: '#015295'}}>{vendorName
        }</h3> 
        } 
        {loading ? (
          <Spinner animation="border" />
        ) : error ? (
          <Alert variant="danger">{error}</Alert>
        ) : (
          <>
            {qrCodeData ? (
              <div>
                <img
                  src={`data:image/png;base64,${qrCodeData}`}
                  alt="Vendor QR Code"
                  style={{ width: '300px', height: 'auto' }}
                />
                <br />
                <Button 
                  onClick={downloadQRCode} 
                  style={{
                    backgroundColor: '#015295',
                    color: '#fff',
                    border: 'none',
                    marginTop: '10px',
                    padding: '10px 20px',
                    fontSize: '16px',
                    cursor: 'pointer'
                  }}
                >
                  Download
                </Button>
              </div>
            ) : (
              <Alert variant="info">No QR Code available.</Alert>
            )}
          </>
        )}
        <Footer />
      </Container>
    </>
  );
};

export default VendorScannerScreen;
