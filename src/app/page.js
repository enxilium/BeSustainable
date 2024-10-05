"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

const handleUpload = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('https://api.openai.com/v1/images', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer YOUR_API_KEY`, // Replace with your actual API key
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to upload image');
    }

    const data = await response.json();
    console.log('Image uploaded successfully:', data);
  } catch (error) {
    console.error('Error uploading image:', error);
  }
};

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const router = useRouter();

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      await handleUpload(file);
      setIsUploaded(true);
    }
  };

  useEffect(() => {
    if (isUploaded) {
      router.push('/redirect-page'); // Replace with your redirect URL
    }
  }, [isUploaded, router]);

  return (
    <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden mx-4">
      <main className="relative flex flex-col gap-8 items-center text-center">
        <Image
          className="dark:invert"
          src="/ecocloset_logo.png"
          alt="ECOCLOSET logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-5xl sm:text-5xl">ECOCLOSET</h1>
        <p>You give us a picture of your worn clothes, and we’ll give it a second life.</p>
        <label className="bg-green-500 text-white py-2 px-4 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 cursor-pointer">
          <input type="file" onChange={handleFileChange} className="hidden" />
          ⤒ Upload
        </label>
      </main>
    </div>
  );
}