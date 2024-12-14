import React, { useState, useEffect } from "react";

const DocumentUploadPage = () => {
  const [documents, setDocuments] = useState({});
  const [selectedFolder, setSelectedFolder] = useState("");
  const [collapsedFolders, setCollapsedFolders] = useState({});
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  // Generate dummy summary and hashtags
  const generateSummaryAndHashtags = (fileName) => {
    const dummySummary = `This is a summary for the file: ${fileName}. It includes key details extracted from the document.`;
    const dummyHashtags = ["#insight", "#document", "#summary"];
    return { summary: dummySummary, hashtags: dummyHashtags };
  };

  // Handle file uploads (via drag-and-drop or file input)
  const handleFileUpload = async (files) => {
    const uploadedFiles = Array.from(files);
    setIsUploading(true);
    setUploadStatus(null);

    for (const file of uploadedFiles) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("folder", selectedFolder || "My Drive");
      formData.append("summary", `Generated summary for ${file.name}`);
      ["#example", "#upload"].forEach(tag => formData.append("hashtags", tag));

      try {
        const response = await fetch("http://127.0.0.1:5002/documents", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();
        if (response.ok) {
          console.log("File uploaded successfully:", result);
          setUploadStatus({ type: 'success', message: `${file.name} uploaded successfully!` });
          setDocuments(prevDocuments => ({
            ...prevDocuments,
            [selectedFolder || "My Drive"]: [
              ...(prevDocuments[selectedFolder || "My Drive"] || []),
              {
                id: result.doc_id,
                name: file.name,
                summary: `Generated summary for ${file.name}`,
                hashtags: ["#example", "#upload"]
              }
            ]
          }));
        } else {
          console.error("Error uploading file:", result.error);
          setUploadStatus({ type: 'error', message: `Error uploading ${file.name}: ${result.error}` });
        }
      } catch (error) {
        console.error("Error:", error);
        setUploadStatus({ type: 'error', message: `Error uploading ${file.name}: ${error.message}` });
      }
    }
    setIsUploading(false);
  };

  const handleDownload = async (documentId, fileName) => {
    try {
      const response = await fetch(`http://127.0.0.1:5002/documents/${documentId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to download file');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading file:', error);
      setUploadStatus({ type: 'error', message: `Error downloading ${fileName}: ${error.message}` });
    }
  };

  // Delete a file
  const handleDeleteFile = async (folder, file) => {
    try {
        const response = await fetch(`http://127.0.0.1:5002/documents/${file.id}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete file');
        }

        // Update local state after successful deletion
        const updatedDocuments = { ...documents };
        updatedDocuments[folder] = updatedDocuments[folder].filter(
            (f) => f.id !== file.id
        );

        // Remove folder if empty
        if (updatedDocuments[folder].length === 0) {
            delete updatedDocuments[folder];
        }

        setDocuments(updatedDocuments);
        setUploadStatus({ type: 'success', message: `${file.name} deleted successfully!` });
    } catch (error) {
        console.error('Error deleting file:', error);
        setUploadStatus({ type: 'error', message: `Error deleting ${file.name}: ${error.message}` });
    }
};

  // Create a new folder
  const handleCreateFolder = () => {
    const folderName = prompt("Enter folder name:");
    if (folderName && !documents[folderName]) {
      setDocuments({ ...documents, [folderName]: [] });
    }
  };

  // Handle drag-and-drop file upload
  const handleDrop = (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleFileUpload(files);
  };

  // Toggle folder collapse
  const toggleFolderCollapse = (folder) => {
    setCollapsedFolders((prevState) => ({
      ...prevState,
      [folder]: !prevState[folder],
    }));
  };

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5002/documents");
        if (response.ok) {
          const data = await response.json();
          setDocuments(data);
        } else {
          console.error("Error fetching documents");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchDocuments();
  }, []); // Empty dependency array means this runs once on mount

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        padding: "2rem",
        maxWidth: "900px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "2rem" }}>My Drive</h1>

      {/* Toolbar for folder management */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "1.5rem",
          alignItems: "center",
          gap: "1rem",
        }}
      >
        {/* Folder actions */}
        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <button
            onClick={handleCreateFolder}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            New Folder
          </button>

          <select
            onChange={(e) => setSelectedFolder(e.target.value)}
            value={selectedFolder}
            style={{
              padding: "0.5rem",
              border: "1px solid #ccc",
              borderRadius: "5px",
              width: "200px",
            }}
          >
            <option value="">My Drive</option>
            {Object.keys(documents).map((folder) => (
              <option key={folder} value={folder}>
                {folder}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Upload status message */}
      {uploadStatus && (
        <div
          style={{
            padding: "1rem",
            marginBottom: "1rem",
            borderRadius: "5px",
            backgroundColor: uploadStatus.type === 'success' ? '#d4edda' : '#f8d7da',
            color: uploadStatus.type === 'success' ? '#155724' : '#721c24',
          }}
        >
          {uploadStatus.message}
        </div>
      )}

      {/* Drag-and-drop area */}
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        style={{
          border: "2px dashed #ccc",
          padding: "2rem",
          textAlign: "center",
          borderRadius: "10px",
          marginBottom: "2rem",
          backgroundColor: "#f9f9f9",
          cursor: "pointer",
          position: "relative",
        }}
      >
        {isUploading ? (
          <div style={{ margin: "1rem 0" }}>
            <p>Uploading... Please wait</p>
          </div>
        ) : (
          <>
            <p style={{ margin: 0 }}>Drag & drop files here, or click to upload</p>
            <input
              type="file"
              multiple
              onChange={(e) => handleFileUpload(e.target.files)}
              style={{ display: "none" }}
              id="fileInput"
            />
            <label
              htmlFor="fileInput"
              style={{
                display: "inline-block",
                marginTop: "1rem",
                padding: "0.5rem 1rem",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Select Files
            </label>
          </>
        )}
      </div>

      {/* Folder and file tree */}
      <div>
        <h2 style={{ marginBottom: "1rem" }}>Folders and Files</h2>
        {Object.keys(documents).length === 0 && (
          <p style={{ textAlign: "center" }}>No files or folders yet.</p>
        )}
        <ul style={{ listStyle: "none", padding: 0 }}>
          {Object.entries(documents).map(([folder, files]) => (
            <li
              key={folder}
              style={{
                marginBottom: "1rem",
                backgroundColor: "#f8f9fa",
                borderRadius: "5px",
                padding: "1rem",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  cursor: "pointer",
                  marginBottom: "0.5rem",
                }}
                onClick={() => toggleFolderCollapse(folder)}
              >
                <span style={{ marginRight: "0.5rem" }}>
                  {collapsedFolders[folder] ? "▶" : "▼"}
                </span>
                <strong>{folder}</strong>
              </div>
              {!collapsedFolders[folder] && (
                <ul style={{ listStyle: "none", paddingLeft: "1.5rem" }}>
                  {files.map((file, index) => (
                    <li
                      key={index}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        padding: "0.5rem",
                        backgroundColor: "white",
                        borderRadius: "3px",
                        marginBottom: "0.5rem",
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: "500" }}>{file.name}</div>
                        <div style={{ fontSize: "0.9em", color: "#666" }}>
                          {file.summary}
                        </div>
                        <div style={{ fontSize: "0.8em", color: "#888" }}>
                          {file.hashtags.join(" ")}
                        </div>
                      </div>
                      <div style={{ display: "flex", gap: "0.5rem" }}>
                        <button
                          onClick={() => handleDownload(file.id, file.name)}
                          style={{
                            padding: "0.3rem 0.8rem",
                            backgroundColor: "#28a745",
                            color: "white",
                            border: "none",
                            borderRadius: "3px",
                            cursor: "pointer",
                          }}
                        >
                          Download
                        </button>
                        <button
                          onClick={() => handleDeleteFile(folder, file)}
                          style={{
                            padding: "0.3rem 0.8rem",
                            backgroundColor: "#dc3545",
                            color: "white",
                            border: "none",
                            borderRadius: "3px",
                            cursor: "pointer",
                          }}
                        >
                          Delete
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DocumentUploadPage;
