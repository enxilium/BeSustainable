"use client"

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

const OPENAI_API_KEY = process.env.NEXT_PUBLIC_OPENAI_API_KEY

const handleUpload = async (file) => {
  try {
    const base64String = await convertToBase64(file);
    
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini", // Note: Replace with "gpt-4o-mini" if it becomes available
        response_format: { type: "text" },
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'text',
                text: `Describe the clothing in the image in the following format: 
                'type': pick the one that suits the clothing best: dress, shoes, jacket, pants, or simply n/a
                'brand': the brand should be in all lowercase with all spaces removed
                'material': choose between leather, cotton, polyester, denim, or simply n/a
                'style': choose between casual, formal, or athletic
                'color': describe the clothing using 1 color. don't use 'light color' or 'dark color' here.
                'state': the condition of the clothing, choose between used and new
                Aftewards, output %%% and then place the descriptions in a list with the following order ['type', 'brand', 'material', 'style', 'color', 'state']. Do not output this string as is. Replace the values within it.
                Output %%% once again, and then output a choice that you think fits best for this article of clothing, if you had to choose.
                Choose between THRIFT, DONATE, DISPOSE. Then, output %%% again, and explain concisely why you made that choice without explicitly referring to yourself.`,
              },
              {
                type: 'image_url',
                image_url: {
                  url: `data:image/jpeg;base64,${base64String}`,
                },
              },
            ],
          }
        ],
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to process image');
    }

    const data = await response.json();
    console.log('Response from OpenAI:', data);
    return data.choices[0].message.content;
  } catch (error) {
    console.error('Error processing image:', error);
    throw error;
  }
};

const convertToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = (error) => reject(error);
  });
};

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [response, setResponse] = useState(null);
  const router = useRouter();
  const [labelText, setLabelText] = useState("⤒ Upload");

  const changeLabelText = () => {
    setLabelText('Processing...'); // Change text when the function is called
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      setIsUploading(true);
      changeLabelText();
      try {
        // Upload the file
        const formData = new FormData();
        formData.append('file', file);
        const uploadResponse = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        });
        const uploadData = await uploadResponse.json();
        
        // Process the image with OpenAI
        const result = await handleUpload(file);
        setResponse(result);
        console.log('OpenAI Response:', result);
        
        // Parse the OpenAI response
      const [description, list, recommendationResult, recommendationExplanation] = result.split('%%%').map(part => part.trim());
      const recommendation = recommendationResult.toUpperCase();
      
      console.log('Recommendation:', recommendation);
      console.log('List from ChatGPT:', list);
      
      let price = null;
      if (recommendation === 'THRIFT') {
        // Parse the string representation of the list into an array
        const dataArray = list.match(/['"]([^'"]*)['"]/g).map(item => item.replace(/['"]/g, ''));
        console.log('Parsed data array:', dataArray);

        // Prepare the data in the correct format
        const requestData = {
          data: dataArray
        };
        console.log('Request data:', requestData);

        // Call the /calcPrice endpoint
        try {
          console.log('Calling /calcPrice endpoint');
          const priceResponse = await fetch('http://127.0.0.1:5000/calcPrice', {
            method: 'POST',
            mode: 'cors',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(requestData),
          });
          const priceData = await priceResponse.json();
          console.log('Price calculation response:', priceData);
          if (priceData.status === 'Success') {
            price = priceData.price;
            console.log('Calculated price:', price);
          } else {
            console.error('Price calculation failed:', priceData.message);
          }
        } catch (error) {
          console.error('Error calculating price:', error);
        }
      }
      
      console.log('Final price before redirect:', price);
      
      // Navigate to the recommendation page
      router.push(`/recommendation?result=${encodeURIComponent(result)}&image=${uploadData.filePath}&price=${price}`);
    } catch (error) {
      console.error('Error handling file:', error);
    } finally {
      setIsUploading(false);
    }
  }
};

  return (
    <div className="inset-0 flex justify-center items-center overflow-hidden mx-4 z-10">
      <main className="relative flex flex-col gap-8 items-center text-center my-20">
        <Image
          className="dark:invert"
          src="/ecocloset_logo.png"
          alt="ECOCLOSET logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-5xl sm:text-5xl">ECOCLOSET</h1>
        <p>You give us a picture of your worn clothes, and we'll give it a second life.</p>
        <label className="bg-green-500 text-white py-2 px-4 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 cursor-pointer">
          <input type="file" accept="image/png, image/jpeg" onChange={handleFileChange} className="hidden" />
          {labelText}
        </label>
        {response && (
          <div>
            
          </div>
        )}
      </main>
    </div>
  );
}