import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

import { NextResponse } from 'next/server';

export const runtime = 'edge';

const s3Client = new S3Client({
  region: process.env.NEXT_PUBLIC_AWS_REGION, // AWS region, e.g., "us-east-1"
  credentials: {
    accessKeyId: process.env.NEXT_PUBLIC_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.NEXT_PUBLIC_AWS_SECRET_ACCESS_KEY,
  },
});

export async function POST(request) {
  const formData = await request.formData();
  const file = formData.get('file');

  if (!file) {
    return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
  }

  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  // Create a unique filename
  const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
  const filename = file.name.replace(/\.[^/.]+$/, "") + '-' + uniqueSuffix + '.' + file.name.split('.').pop();

  try {
    // Upload the file to AWS S3
    const uploadParams = {
      Bucket: process.env.NEXT_PUBLIC_AWS_BUCKET_NAME, // Your S3 bucket name
      Key: `${filename}`, // File path in the bucket
      Body: buffer, // File buffer
      ContentType: file.type, // MIME type of the file
    };

    const command = new PutObjectCommand(uploadParams);
    await s3Client.send(command);

    const fileUrl = `https://${process.env.NEXT_PUBLIC_AWS_BUCKET_NAME}.s3.${process.env.NEXT_PUBLIC_AWS_REGION}.amazonaws.com/uploads/${filename}`;

    return NextResponse.json({ message: 'File uploaded successfully', filePath: fileUrl });
  }catch (error) {

    console.log(error.message)
  return NextResponse.json({ error: 'Failed to upload file', details: error.message }, { status: 500 });
  }
}

