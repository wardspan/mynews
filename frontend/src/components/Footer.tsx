'use client';

import React from 'react';
import {
  Box,
  Container,
  Stack,
  Text,
  Link,
  useColorModeValue,
} from '@chakra-ui/react';

const Footer: React.FC = () => {
  return (
    <Box
      bg={useColorModeValue('gray.50', 'gray.900')}
      color={useColorModeValue('gray.700', 'gray.200')}
      mt="auto">
      <Container
        as={Stack}
        maxW={'6xl'}
        py={4}
        direction={{ base: 'column', md: 'row' }}
        spacing={4}
        justify={{ base: 'center', md: 'space-between' }}
        align={{ base: 'center', md: 'center' }}>
        <Text>© {new Date().getFullYear()} MyNews. All rights reserved</Text>
        <Stack direction={'row'} spacing={6}>
          <Link href={'#'}>Privacy</Link>
          <Link href={'#'}>Terms</Link>
          <Link href={'#'}>About</Link>
        </Stack>
      </Container>
    </Box>
  );
};

export default Footer;