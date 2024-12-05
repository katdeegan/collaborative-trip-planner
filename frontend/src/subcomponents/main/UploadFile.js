import React, { useState } from 'react';
import axios from 'axios';
import '../styles/form-styles.css'; 

const FileUpload = ({userId, tripId}) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [filePath, setFilePath] = useState('');

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

    try {
      setUploading(true);
      const response = await axios.post('YOUR_BACKEND_API_URL', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploading(false);
      if (response.data && response.data.filePath) {
        setFilePath(response.data.filePath);
        alert('File uploaded successfully!');
      } else {
        alert('Upload failed!');
      }
    } catch (error) {
      setUploading(false);
      alert('Error uploading file: ' + error.message);
    }
  };

  return (
    <div>
      <h2>Upload Trip Document</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {filePath && (
        <div>
          <p>File uploaded successfully. File path: {filePath}</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
