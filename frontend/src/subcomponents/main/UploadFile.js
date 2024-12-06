import React, { useState, useEffect} from 'react';
import { useNavigate  } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';  
import { faArrowLeft  } from '@fortawesome/free-solid-svg-icons'; 
import axios from 'axios';
import '../styles/form-styles.css'; 

const FileUpload = ({userId, tripId}) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [filePath, setFilePath] = useState('');

  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getTripDocsUrl = `http://127.0.0.1:2000/apiv1/getDocuments/${tripId}`
  const uploadTripDocUrl = `http://127.0.0.1:2000/apiv1/addDocument/${tripId}`

  const navigate = useNavigate();

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(getTripDocsUrl);  
      setDocuments(response.data.documents);
      setLoading(false);  
    } catch (err) {
      setError('Failed to fetch trip documents.');
      setLoading(false);
    }

  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file upload
  const handleFileUpload = async () => {
    if (!file) {
      alert('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    console.log(formData);

    try {
      setUploading(true);
      const response = await axios.post(uploadTripDocUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploading(false);
      console.log('File uploaded successfully:', response.data);
    } catch (error) {
      setUploading(false);
      alert('Error uploading file: ' + error.message);
    }
    setFile(null);
    setFilePath('');
    fetchDocuments();
  };

  return (
    <div>
            <button
      style={{
        fontSize: '16px',
        backgroundColor: 'transparent', 
        color: 'blue',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
      }}
      onClick={() => navigate("/tripDetails")}
    >
      <FontAwesomeIcon icon={faArrowLeft} style={{ marginRight: '8px' }} />
      Return to Trip Days
    </button>
      <h2>Upload Trip Document</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      <div>
        <h2>Trip Documents:</h2>
        {loading ? (
          <p>Loading documents...</p>  
        ) : error ? (
          <p>{error}</p>
        ) : (
          <ul>
            {documents.map((doc, index) => (
              <li key={index}>
                <a href={doc.url} target="_blank" rel="noopener noreferrer">
                  {doc.name}
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>

      {filePath && (
        <div>
          <p>File uploaded successfully. File path: {filePath}</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
