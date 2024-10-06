'use client';

import React, { useState, useEffect } from 'react';
import { Suspense } from 'react';

import { useSearchParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';

function RecommendationContent(){
  const [recommendation, setRecommendation] = useState('');
  const [value, setValue] = useState('N/A');
  const [imagePath, setImagePath] = useState('');
  const [analysis, setAnalysis] = useState('');
  const searchParams = useSearchParams();

  useEffect(() => {
    const result = searchParams.get('result');
    const image = searchParams.get('image');
    const price = searchParams.get('price');
    
    console.log('Received price:', price); // Log the received price
    
    if (result) {
      console.log('Raw result:', result);

      const [description, list, recommendationResult] = result.split('%%%').map(part => part.trim());
      const recommendationUpper = recommendationResult.toUpperCase();
      setRecommendation(recommendationUpper);
      
      // Parse the description
      const details = {};
      description.split('\n').forEach(line => {
        const [key, value] = line.split(':').map(part => part.trim());
        details[key.replace(/'/g, '')] = value;
      });

      // Set the analysis using the parsed details
      setAnalysis(`Type: ${details.type}, Brand: ${details.brand}, Material: ${details.material}, Style: ${details.style}, Color: ${details.color}, State: ${details.state}`);
      
      // Set value only if recommendation is THRIFT and price is available
      if (recommendationUpper === 'THRIFT' && price) {
        console.log('Setting price for THRIFT item:', price);
        setValue(parseFloat(price));
      } else {
        console.log('Setting price to N/A');
        setValue('N/A');
      }
    }

    if (image) {
      setImagePath(image);
    }
  }, [searchParams]);

  console.log('Final set value:', value); // Log the final set value


  return (
      <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden p-4">
        <div className="bg-white rounded-[2rem] shadow-lg p-8 max-w-md w-full">
          <main className="flex flex-col items-center text-center">
            <h2 className="text-xl mb-4">Your uploaded photo:</h2>
            <div className="w-64 h-64 bg-gray-100 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
              {imagePath ? (
                <Image src={imagePath} alt="Your clothing" width={256} height={256} objectFit="contain" />
              ) : (
                <span className="block text-sm text-gray-500">No image uploaded</span>
              )}
            </div>

            <h3 className="text-lg font-semibold mb-1">Designation:</h3>
            <p className="text-4xl font-bold mb-2">{recommendation}</p>

            <h3 className="text-lg font-semibold mb-1">Value:</h3>
            <p className="text-4xl font-bold mb-2">
              {value === 'N/A' ? 'N/A' : `$${value.toFixed(2)}`}
            </p>

            <h3 className="text-lg font-semibold mb-1">Analysis:</h3>
            <p className="text-sm mb-6">{analysis}</p>      

            <Link href={{pathname: "/dashboard", query: { "recommendation":  recommendation, "price": value}}} className="bg-green-500 text-white py-2 px-4 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 transition duration-300 ease-in-out">
              Go to Dashboard
            </Link>
          </main>
        </div>
      </div>
  );
}

export default function RecommendationPage() {
  return (
    <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden p-4">
      <Suspense fallback={<div>Loading...</div>}>
        <RecommendationContent />
      </Suspense>
    </div>
  );
}