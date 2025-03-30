'use client';

import { useState } from 'react';
import { 
  Box, 
  Heading, 
  Text, 
  Button, 
  HStack, 
  useToast, 
  Menu, 
  MenuButton, 
  MenuList, 
  MenuItem,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Icon,
  Flex
} from '@chakra-ui/react';
import { ChevronDownIcon, RepeatIcon } from '@chakra-ui/icons';
import { useQuery } from 'react-query';
import Layout from '../Layout';
import ArticleGrid from '../articles/ArticleGrid';
import { articles as articlesApi } from '../../services/api';
import { Article, CategoryInfo, SourceInfo } from '../../types/article';

const HomePage = () => {
  const toast = useToast();
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [activeSource, setActiveSource] = useState<string>('all');
  
  // Fetch available categories
  const { data: categoriesData } = useQuery<{ data: CategoryInfo[] }>('categories', articlesApi.getCategories, {
    staleTime: 1000 * 60 * 60, // 1 hour
  });
  
  // Fetch available sources
  const { data: sourcesData } = useQuery<{ data: SourceInfo[] }>('sources', articlesApi.getSources, {
    staleTime: 1000 * 60 * 60, // 1 hour
  });
  
  // Fetch latest articles
  const { 
    data: articlesData, 
    isLoading, 
    isError, 
    refetch 
  } = useQuery<{ data: Article[] }>(
    ['latest-articles', activeCategory, activeSource],
    () => {
      const params: any = {
        limit: 20,
        refresh: false
      };
      
      if (activeCategory !== 'all') {
        params.categories = [activeCategory];
      }
      
      if (activeSource !== 'all') {
        params.sources = [activeSource];
      }
      
      return articlesApi.getLatest(params);
    },
    {
      staleTime: 1000 * 60 * 5, // 5 minutes
    }
  );
  
  // Refresh articles with latest data from sources
  const refreshArticles = async () => {
    try {
      const params: any = {
        limit: 20,
        refresh: true
      };
      
      if (activeCategory !== 'all') {
        params.categories = [activeCategory];
      }
      
      if (activeSource !== 'all') {
        params.sources = [activeSource];
      }
      
      await articlesApi.getLatest(params);
      await refetch();
      
      toast({
        title: 'Articles refreshed',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Failed to refresh articles', error);
      toast({
        title: 'Failed to refresh articles',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };
  
  const categories = categoriesData?.data || [];
  const sources = sourcesData?.data || [];
  const articles = articlesData?.data || [];
  
  // Calculate index of category tab to select
  const activeTabIndex = (() => {
    if (activeCategory === 'all') return 0;
    
    const index = categories.findIndex(c => c.id === activeCategory);
    return index === -1 ? 0 : index + 1; // +1 because "All" tab is at index 0
  })();
  
  return (
    <Layout>
      <Box>
        <Flex direction={{ base: 'column', md: 'row' }} justify="space-between" align={{ base: 'start', md: 'center' }} mb={6}>
          <Box mb={{ base: 4, md: 0 }}>
            <Heading as="h1" size="xl" mb={2}>
              Latest News
            </Heading>
            <Text color="gray.600">
              Stay updated with the latest articles from various sources
            </Text>
          </Box>
          
          <HStack>
            <Button 
              leftIcon={<Icon as={RepeatIcon} />} 
              colorScheme="blue" 
              onClick={refreshArticles}
              isLoading={isLoading}
            >
              Refresh
            </Button>
            
            <Menu>
              <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                {activeSource === 'all' ? 'All Sources' : 
                  sources.find(s => s.id === activeSource)?.name || activeSource}
              </MenuButton>
              <MenuList>
                <MenuItem onClick={() => setActiveSource('all')}>All Sources</MenuItem>
                {sources.map(source => (
                  <MenuItem 
                    key={source.id} 
                    onClick={() => setActiveSource(source.id)}
                    isDisabled={!source.enabled}
                  >
                    {source.name}
                  </MenuItem>
                ))}
              </MenuList>
            </Menu>
          </HStack>
        </Flex>
        
        <Tabs 
          variant="soft-rounded" 
          colorScheme="blue" 
          mb={6} 
          index={activeTabIndex}
          onChange={(index) => {
            if (index === 0) {
              setActiveCategory('all');
            } else {
              const category = categories[index - 1];
              if (category) {
                setActiveCategory(category.id);
              }
            }
          }}
        >
          <TabList overflowX="auto" py={2}>
            <Tab>All</Tab>
            {categories.map(category => (
              <Tab key={category.id}>
                {category.name}
              </Tab>
            ))}
          </TabList>
          
          <TabPanels>
            <TabPanel px={0}>
              <ArticleGrid 
                articles={articles} 
                isLoading={isLoading} 
                isError={isError} 
              />
            </TabPanel>
            {/* We don't actually need separate tab panels since we're using the same component with different data */}
            {categories.map(category => (
              <TabPanel key={category.id} px={0}>
                <ArticleGrid 
                  articles={articles} 
                  isLoading={isLoading} 
                  isError={isError} 
                />
              </TabPanel>
            ))}
          </TabPanels>
        </Tabs>
      </Box>
    </Layout>
  );
};

export default HomePage;