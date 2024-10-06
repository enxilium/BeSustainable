import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    console.log('API Key:', process.env.OPENAI_API_KEY); // Log the API key (be careful with this in production)
    
    const { base64Image } = await req.json();

    if (!process.env.OPENAI_API_KEY) {
      console.error('OPENAI_API_KEY is not set');
      return NextResponse.json({ error: 'API key is not configured' }, { status: 500 });
    }

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4-vision-preview",
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
                Output %%% once again, and then output a choice that you think fits best for this article of clothing, if you had to choose. Do not explain why, simply output your choice.
                Choose between THRIFT, DONATE, DISPOSE`,
              },
              {
                type: 'image_url',
                image_url: {
                  url: `data:image/jpeg;base64,${base64Image}`,
                },
              },
            ],
          }
        ],
      }),
    });

    console.log('OpenAI API Response Status:', response.status);

    if (!response.ok) {
      const errorData = await response.json();
      console.error('OpenAI API error:', errorData);
      return NextResponse.json({ error: 'Failed to process image', details: errorData }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in OpenAI API route:', error);
    return NextResponse.json({ error: 'Internal server error', details: error.message }, { status: 500 });
  }
}