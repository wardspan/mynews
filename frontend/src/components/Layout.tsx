'use client';
import React, { ReactNode } from 'react';
import { Box, Container, Flex } from '@chakra-ui/react';
import Navbar from './Navbar';
import Footer from './Footer';
import { useAuth } from '../contexts/AuthContext';
import LoadingScreen from './LoadingScreen';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { loading } = useAuth();

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <Flex direction="column" minH="100vh">
      <Navbar />
      <Box as="main" flex="1" py={8}>
        <Container maxW="container.xl">{children}</Container>
      </Box>
      <Footer />
    </Flex>
  );
};

export default Layout;