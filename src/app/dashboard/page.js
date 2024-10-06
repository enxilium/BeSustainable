'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { ArrowLeft, Info } from 'lucide-react';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';


export default function AboutPage() {
  const [selectedItem, setSelectedItem] = useState(null);
  let [savedMoney, setSavedMoney] = useState(0);
  let [items, setItem] = useState([]);

  const searchParams = useSearchParams();
  const recommendation = searchParams.get('recommendation'); 
  const price = searchParams.get('price'); 

    
  if (recommendation == "THRIFT"){

    useEffect(() => {
      const fetchData = async () => {
        try {
          console.log('Calling /thrift endpoint');
          const res = await fetch('http://127.0.0.1:5000/thrift', {
            method: 'GET',
            mode: 'cors',
            headers: {
              'Accept': 'application/json',
              'Access-Control-Allow-Origin': '*'
            },
          });
          const data = await res.json();

          setItem(data["data"]);
        }
        
        catch (error) {
            console.error('Error handling file:', error);
        }
      }

      fetchData();

      setSavedMoney(Number(price).toFixed(2));
    }, []);

  }

  else if (recommendation == "DONATE"){

    useEffect(() => {
      const fetchData = async () => {
        try {
          console.log('Calling /donation endpoint');
          const res = await fetch('http://127.0.0.1:5000/donation', {
            method: 'GET',
            mode: 'cors',
            headers: {
              'Accept': 'application/json',
              'Access-Control-Allow-Origin': '*'
            },
          });
          const data = await res.json();

          setItem(data["data"]);
        }
        
        catch (error) {
            console.error('Error handling file:', error);
        }
      }

      fetchData();

      setSavedMoney(recommendation);
    }, [recommendation, price]);

  }

  

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className="absolute inset-0 flex justify-center items-center h-svh overflow-hidden mx-4">
        <main className="relative flex flex-col gap-8 items-center text-center w-full max-w-md">
          <Image
            className="dark:invert"
            src="/ecocloset_logo.png"
            alt="ECOCLOSET logo"
            width={180}
            height={38}
            priority
          />
          <h1 className="text-5xl sm:text-5xl">Summary</h1>
          
          <div className="bg-green-100 rounded-lg p-4 w-full">
            <h2 className="text-2xl font-bold text-green-800">
              {recommendation === "THRIFT" ? "Total Savings" : recommendation}
            </h2>
            
            {recommendation === "THRIFT" && (
              <p className="text-4xl font-bold text-green-600">${savedMoney}</p>
            )}
          </div>
          
          <div className="w-full">
            <h3 className="text-xl font-bold mb-4">Your Items</h3>
            <ul className="space-y-4">
              {items.map((item) => (
                <li key={item.id} className="bg-white rounded-lg shadow-md p-4 flex justify-between items-center">
                  <span>{item.name}</span>
                  <button
                    onClick={() => setSelectedItem(item)}
                    className="bg-blue-500 text-white p-2 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
                  >
                    <Info size={20} />
                  </button>
                </li>
              ))}
            </ul>
          </div>
          
          {selectedItem && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
              <div className="bg-white rounded-lg p-6 max-w-sm w-full">
                <h4 className="text-xl font-bold mb-2">{selectedItem.name}</h4>
                <p className="mb-4">{selectedItem.address}</p>
                <button
                  onClick={() => setSelectedItem(null)}
                  className="bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400"
                >
                  Close
                </button>
              </div>
            </div>
          )}

          <a href='/'>
            <button
              className="bg-green-500 text-white py-2 px-4 rounded-md shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 flex items-center"
            >
              <ArrowLeft size={20} className="mr-2" />
              Back to Home
            </button>
          </a>
        </main>
      </div>
    </Suspense>
  );
}