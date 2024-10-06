"use client"

import React from 'react';
import styled from 'styled-components';
import Image from 'next/image';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background: #f5f5f5; /* Light background color for contrast */
`;

const Header = styled.h1`
  font-size: 3rem;
  color: #2d6a4f; /* Green color for a sustainability theme */
  margin-bottom: 1rem;
  text-align: center;
`;

const Subtitle = styled.h2`
  font-size: 1.5rem;
  color: #2d6a4f;
  text-align: center;
  margin-bottom: 2rem;
`;

const StatsContainer = styled.div`
  max-width: 800px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  margin-bottom: 3rem;
`;

const StatItem = styled.div`
  margin-bottom: 1.5rem;
`;

const StatNumber = styled.span`
  font-size: 2rem;
  font-weight: bold;
  color: #1b4332;
`;

const StatDescription = styled.p`
  font-size: 1rem;
  color: #555;
`;

const Footer = styled.footer`
  margin-top: 2rem;
  text-align: center;
  color: #555;
  font-size: 0.9rem;
`;

const About = () => {
  return (
    <Container>
      {/* Header Section */}
      <Header>About Ecocloset</Header>
      <Subtitle>
        Giving Clothes a Second Life for a Greener Future
      </Subtitle>

      {/* Statistics Section */}
      <StatsContainer>
        <StatItem>
          <StatNumber>85%</StatNumber>
          <StatDescription>
            of all textiles thrown away in the U.S. are either dumped into
            landfills or burned – a major contributor to environmental pollution.
          </StatDescription>
        </StatItem>
        <StatItem>
          <StatNumber>700 Gallons</StatNumber>
          <StatDescription>
            of water are required to produce a single cotton t-shirt. Imagine how
            much water can be saved by extending the life of just one item.
          </StatDescription>
        </StatItem>
        <StatItem>
          <StatNumber>5%</StatNumber>
          <StatDescription>
            of global carbon emissions are produced by the fashion industry.
            Repurposing or donating clothes can significantly reduce this impact.
          </StatDescription>
        </StatItem>
      </StatsContainer>

      {/* Message Section */}
      <Subtitle>
        Join us in promoting sustainability by giving your clothing a second
        chance. Donate or sell to thrift stores and make a positive impact!
      </Subtitle>

      {/* Footer Section */}
      <Footer>
        <p>© 2024 Ecocloset. All rights reserved.</p>
        <p>
          Designed with sustainability in mind. Contact us at{' '}
          <a href="mailto:contact@ecocloset.com" style={{ color: '#2d6a4f' }}>
            contact@ecocloset.com
          </a>
        </p>
      </Footer>
    </Container>
  );
};

export default About;
