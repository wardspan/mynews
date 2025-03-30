'use client';

import React from 'react';
import {
  Box,
  Heading,
  Text,
  Stack,
  useColorModeValue,
  Image,
  HStack,
  Tag,
  Link,
  Flex
} from '@chakra-ui/react';
import NextLink from 'next/link';
import { format } from 'date-fns';
import { Article } from '../../types/article';

const DEFAULT_IMAGE = 'https://via.placeholder.com/800x400?text=MyNews';

interface ArticleCardProps {
  article: Article;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article }) => {
  // Extract article data
  const {
    id,
    title,
    synopsis,
    author,
    source,
    published_date,
    image_url,
    categories = []
  } = article;

  // Format the date
  const formattedDate = published_date ? 
    format(new Date(published_date), 'MMM dd, yyyy') : 
    'Unknown date';

  return (
    <NextLink href={`/article/${id}`} passHref>
      <Box
        as={Link}
        maxW={'445px'}
        w={'full'}
        bg={useColorModeValue('white', 'gray.900')}
        boxShadow={'md'}
        rounded={'md'}
        p={6}
        overflow={'hidden'}
        _hover={{ 
          transform: 'translateY(-5px)',
          transition: 'all .2s ease-in-out',
          boxShadow: 'lg'
        }}
        transition="all 0.2s"
        height="100%"
        display="flex"
        flexDirection="column"
        textDecoration="none"
      >
        {image_url && (
          <Box
            h={'210px'}
            bg={'gray.100'}
            mt={-6}
            mx={-6}
            mb={6}
            pos={'relative'}>
            <Image
              src={image_url || DEFAULT_IMAGE}
              fallbackSrc={DEFAULT_IMAGE}
              objectFit="cover"
              width="100%"
              height="100%"
              alt={title}
            />
          </Box>
        )}
        <Stack flex={1} display="flex" flexDirection="column">
          <Flex mb={2}>
            {categories.slice(0, 3).map((category, index) => (
              <Tag key={index} colorScheme="blue" mr={2} size="sm">
                {category}
              </Tag>
            ))}
          </Flex>
          <Heading
            color={useColorModeValue('gray.700', 'white')}
            fontSize={'xl'}
            fontFamily={'body'}
            noOfLines={2}
          >
            {title}
          </Heading>
          <Text color={'gray.500'} noOfLines={3} mb={4}>
            {synopsis || 'No description available'}
          </Text>
          <Stack
            mt="auto"
            direction={'row'}
            spacing={4}
            align={'center'}
          >
            <Stack direction={'column'} spacing={0} fontSize={'sm'}>
              <Text fontWeight={600}>{source}</Text>
              <Text color={'gray.500'}>{formattedDate}</Text>
            </Stack>
          </Stack>
        </Stack>
      </Box>
    </NextLink>
  );
};

export default ArticleCard;