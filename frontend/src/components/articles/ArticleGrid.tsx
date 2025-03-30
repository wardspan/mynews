'use client';

import React from 'react';
import { Grid, Text, Center, Spinner, Button, VStack } from '@chakra-ui/react';
import ArticleCard from './ArticleCard';
import { Article } from '../../types/article';

interface ArticleGridProps {
  articles: Article[];
  isLoading: boolean;
  isError: boolean;
  hasMore?: boolean;
  loadMore?: () => void;
}

const ArticleGrid: React.FC<ArticleGridProps> = ({ 
  articles, 
  isLoading, 
  isError, 
  hasMore = false, 
  loadMore = undefined
}) => {
  if (isLoading && articles.length === 0) {
    return (
      <Center py={10}>
        <VStack spacing={4}>
          <Spinner size="xl" color="blue.500" />
          <Text>Loading articles...</Text>
        </VStack>
      </Center>
    );
  }

  if (isError) {
    return (
      <Center py={10}>
        <Text color="red.500">Error loading articles. Please try again later.</Text>
      </Center>
    );
  }

  if (articles.length === 0) {
    return (
      <Center py={10}>
        <Text>No articles found.</Text>
      </Center>
    );
  }

  return (
    <VStack spacing={6} align="stretch">
      <Grid
        templateColumns={{
          base: 'repeat(1, 1fr)',
          sm: 'repeat(2, 1fr)',
          md: 'repeat(3, 1fr)',
          lg: 'repeat(4, 1fr)',
        }}
        gap={6}
      >
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </Grid>
      
      {hasMore && loadMore && (
        <Center py={6}>
          <Button
            isLoading={isLoading}
            onClick={loadMore}
            colorScheme="blue"
          >
            Load More
          </Button>
        </Center>
      )}
    </VStack>
  );
};

export default ArticleGrid;