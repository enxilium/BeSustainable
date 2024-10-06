"use client";

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import styled from 'styled-components';

// Styled components for page layout and styles
const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f5f5; /* Light background color for the page */
  text-align: center;
`;

const LogoWrapper = styled.div`
  margin-bottom: 2rem;
`;

const ComingSoonText = styled.h1`
  font-size: 3rem;
  color: #2d6a4f; /* Green color for the text */
  margin-bottom: 1rem;
`;

const Message = styled.p`
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 2rem;
`;

const StyledButton = styled(Link)`
  padding: 10px 20px;
  font-size: 1rem;
  background: #2d6a4f;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.3s ease;

  &:hover {
    background: #1b4332; /* Darker green on hover */
  }
`;

export default function ComingSoon() {
  return (
    <Container>
      {/* Logo Image */}
      <LogoWrapper>
        <Image
          src="/ecocloset_logo.png" // Path to your logo image in the public folder
          alt="ECOCLOSET logo"
          width={150}
          height={50}
          priority
        />
      </LogoWrapper>

      {/* Coming Soon Message */}
      <ComingSoonText>Coming Soon!</ComingSoonText>

      {/* Additional message or description */}
      <Message>
        We're working hard to bring you something amazing. Stay tuned for updates!
      </Message>

      {/* Back to Home button */}
      <StyledButton href="/">Back to Home</StyledButton>
    </Container>
  );
}