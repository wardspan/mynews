import { defineStyle, defineStyleConfig, createMultiStyleConfigHelpers } from '@chakra-ui/react'

// Define the base configuration
const config = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

// Define the theme
const theme = {
  config,
  fonts: {
    heading: `'Inter', sans-serif`,
    body: `'Inter', sans-serif`,
  },
  colors: {
    brand: {
      50: '#E6F6FF',
      100: '#BAE3FF',
      200: '#7CC4FA',
      300: '#47A3F3',
      400: '#2186EB',
      500: '#0967D2',
      600: '#0552B5',
      700: '#03449E',
      800: '#01337D',
      900: '#002159',
    },
  },
  components: {
    Button: defineStyleConfig({
      baseStyle: {
        fontWeight: 'medium',
        borderRadius: 'md',
      },
    }),
    Heading: defineStyleConfig({
      baseStyle: {
        fontWeight: '600',
      },
    }),
    Tag: defineStyleConfig({
      baseStyle: {
        borderRadius: 'full',
      },
    }),
  },
};

export default theme;