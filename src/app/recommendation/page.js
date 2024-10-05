'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RecommendationPage() {
  const [recommendation, setRecommendation] = useState('THRIFT');
  const [value, setValue] = useState(39.99);
  const [uploadedImage, setUploadedImage] = useState(null);
  const router = useRouter();

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => setUploadedImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden p-4">
        <div className="bg-white rounded-[2rem] shadow-lg p-8 max-w-md w-full">        <main className="flex flex-col items-center text-center">
          <h2 className="text-xl mb-4">Your uploaded photo:</h2>
          <div className="w-64 h-64 bg-gray-100 rounded-lg mb-4 flex items-center justify-center">
            {uploadedImage ? (
              <img src={uploadedImage} alt="Uploaded clothing" className="max-w-full max-h-full object-contain" />
            ) : (
              <label className="cursor-pointer text-center">
                <span className="block text-sm text-gray-500">Click to upload an image</span>
                <input type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
              </label>
            )}
          </div>

          <h3 className="text-lg font-semibold mb-1">Designation:</h3>
          <p className="text-4xl font-bold mb-2">{recommendation}</p>

          <h3 className="text-lg font-semibold mb-1">Value:</h3>
          <p className="text-4xl font-bold mb-2">${value.toFixed(2)}</p>

          <h3 className="text-lg font-semibold mb-1">Analysis:</h3>
          <p className="text-sm">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
            incididunt ut labore et dolore magna aliqua.
          </p>
        </main>
      </div>
    </div>
  );
}