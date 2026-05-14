import { useRef, useState } from 'react';
import { Upload, File, FileText, X, Presentation } from 'lucide-react';

interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: string;
}

export function FileUploader() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return <File className="w-5 h-5 text-red-500" />;
    if (type.includes('word') || type.includes('document')) return <FileText className="w-5 h-5 text-blue-500" />;
    if (type.includes('presentation') || type.includes('powerpoint')) return <Presentation className="w-5 h-5 text-orange-500" />;
    return <FileText className="w-5 h-5 text-gray-500" />;
  };

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;

    const acceptedTypes = [
      'application/pdf',
      'text/plain',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      'application/vnd.ms-powerpoint',
    ];

    const newFiles: UploadedFile[] = [];

    Array.from(fileList).forEach((file) => {
      if (acceptedTypes.includes(file.type) || file.name.endsWith('.txt')) {
        newFiles.push({
          id: Math.random().toString(36).substr(2, 9),
          name: file.name,
          size: file.size,
          type: file.type,
          uploadedAt: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        });
      }
    });

    setFiles((prev) => [...prev, ...newFiles]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter((file) => file.id !== id));
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 border-l border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-white">
        <h2 className="font-semibold text-gray-900">File Uploads</h2>
        <p className="text-sm text-gray-500 mt-1">PDF, TXT, DOCX, PPT</p>
      </div>

      {/* Upload Area */}
      <div className="p-6">
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
            isDragging
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50'
          }`}
        >
          <div className="flex flex-col items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
              <Upload className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">Drop files here</p>
              <p className="text-sm text-gray-500 mt-1">or click to browse</p>
            </div>
            <p className="text-xs text-gray-400">Supports PDF, TXT, DOCX, PPT</p>
          </div>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.txt,.doc,.docx,.ppt,.pptx"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* Files List */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <div className="space-y-3">
          {files.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-sm text-gray-500">No files uploaded yet</p>
            </div>
          ) : (
            files.map((file) => (
              <div
                key={file.id}
                className="bg-white rounded-lg p-4 border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 mt-1">{getFileIcon(file.type)}</div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-sm text-gray-900 truncate">{file.name}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                      <span className="text-gray-300">•</span>
                      <p className="text-xs text-gray-500">{file.uploadedAt}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFile(file.id)}
                    className="flex-shrink-0 w-6 h-6 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Footer Stats */}
      {files.length > 0 && (
        <div className="px-6 py-4 border-t border-gray-200 bg-white">
          <p className="text-sm text-gray-600">
            {files.length} {files.length === 1 ? 'file' : 'files'} uploaded
          </p>
        </div>
      )}
    </div>
  );
}
