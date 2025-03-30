'use client';

import React from 'react';
import { 
  Box, 
  Flex, 
  Text, 
  IconButton, 
  Button, 
  Stack, 
  Collapse, 
  Icon, 
  Link, 
  useColorModeValue, 
  useDisclosure,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider
} from '@chakra-ui/react';
import { HamburgerIcon, CloseIcon, ChevronDownIcon, ChevronRightIcon } from '@chakra-ui/icons';
import NextLink from 'next/link';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { isOpen, onToggle } = useDisclosure();
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <Box>
      <Flex
        bg={useColorModeValue('white', 'gray.800')}
        color={useColorModeValue('gray.600', 'white')}
        minH={'60px'}
        py={{ base: 2 }}
        px={{ base: 4 }}
        borderBottom={1}
        borderStyle={'solid'}
        borderColor={useColorModeValue('gray.200', 'gray.900')}
        align={'center'}>
        <Flex
          flex={{ base: 1, md: 'auto' }}
          ml={{ base: -2 }}
          display={{ base: 'flex', md: 'none' }}>
          <IconButton
            onClick={onToggle}
            icon={
              isOpen ? <CloseIcon w={3} h={3} /> : <HamburgerIcon w={5} h={5} />
            }
            variant={'ghost'}
            aria-label={'Toggle Navigation'}
          />
        </Flex>
        <Flex flex={{ base: 1 }} justify={{ base: 'center', md: 'start' }}>
          <NextLink href="/" passHref>
            <Text
              as={Link}
              textAlign={useColorModeValue('left', 'center')}
              fontFamily={'heading'}
              color={useColorModeValue('gray.800', 'white')}
              fontWeight="bold"
              fontSize="xl">
              MyNews
            </Text>
          </NextLink>

          <Flex display={{ base: 'none', md: 'flex' }} ml={10}>
            <DesktopNav />
          </Flex>
        </Flex>

        <Stack
          flex={{ base: 1, md: 0 }}
          justify={'flex-end'}
          direction={'row'}
          spacing={6}>
          {isAuthenticated ? (
            <Menu>
              <MenuButton
                as={Button}
                rounded={'full'}
                variant={'link'}
                cursor={'pointer'}
                minW={0}>
                <Avatar
                  size={'sm'}
                  name={user?.name || 'User'}
                />
              </MenuButton>
              <MenuList>
                <NextLink href="/profile" passHref>
                  <MenuItem as={Link}>Profile</MenuItem>
                </NextLink>
                <NextLink href="/saved-articles" passHref>
                  <MenuItem as={Link}>Saved Articles</MenuItem>
                </NextLink>
                <MenuDivider />
                <MenuItem onClick={logout}>Sign Out</MenuItem>
              </MenuList>
            </Menu>
          ) : (
            <>
              <NextLink href="/login" passHref>
                <Button
                  as={Link}
                  fontSize={'sm'}
                  fontWeight={400}
                  variant={'link'}>
                  Sign In
                </Button>
              </NextLink>
              <NextLink href="/register" passHref>
                <Button
                  as={Link}
                  display={{ base: 'none', md: 'inline-flex' }}
                  fontSize={'sm'}
                  fontWeight={600}
                  color={'white'}
                  bg={'blue.400'}
                  _hover={{
                    bg: 'blue.300',
                  }}>
                  Sign Up
                </Button>
              </NextLink>
            </>
          )}
        </Stack>
      </Flex>

      <Collapse in={isOpen} animateOpacity>
        <MobileNav />
      </Collapse>
    </Box>
  );
};

const DesktopNav: React.FC = () => {
  const linkColor = useColorModeValue('gray.600', 'gray.200');
  const linkHoverColor = useColorModeValue('gray.800', 'white');
  const { isAuthenticated } = useAuth();

  return (
    <Stack direction={'row'} spacing={4}>
      <NextLink href="/" passHref>
        <Link
          p={2}
          fontSize={'sm'}
          fontWeight={500}
          color={linkColor}
          _hover={{
            textDecoration: 'none',
            color: linkHoverColor,
          }}>
          Home
        </Link>
      </NextLink>
      {isAuthenticated && (
        <>
          <NextLink href="/categories" passHref>
            <Link
              p={2}
              fontSize={'sm'}
              fontWeight={500}
              color={linkColor}
              _hover={{
                textDecoration: 'none',
                color: linkHoverColor,
              }}>
              Categories
            </Link>
          </NextLink>
          <NextLink href="/saved-articles" passHref>
            <Link
              p={2}
              fontSize={'sm'}
              fontWeight={500}
              color={linkColor}
              _hover={{
                textDecoration: 'none',
                color: linkHoverColor,
              }}>
              Saved Articles
            </Link>
          </NextLink>
        </>
      )}
    </Stack>
  );
};

interface NavItem {
  label: string;
  href?: string;
  children?: Array<NavItem>;
}

const MobileNav: React.FC = () => {
  const { isAuthenticated } = useAuth();
  
  return (
    <Stack
      bg={useColorModeValue('white', 'gray.800')}
      p={4}
      display={{ md: 'none' }}>
      <MobileNavItem label="Home" href="/" />
      {isAuthenticated && (
        <>
          <MobileNavItem label="Categories" href="/categories" />
          <MobileNavItem label="Saved Articles" href="/saved-articles" />
          <MobileNavItem label="Profile" href="/profile" />
        </>
      )}
    </Stack>
  );
};

interface MobileNavItemProps {
  label: string;
  children?: Array<NavItem>;
  href?: string;
}

const MobileNavItem: React.FC<MobileNavItemProps> = ({ label, children, href }) => {
  const { isOpen, onToggle } = useDisclosure();

  return (
    <Stack spacing={4} onClick={children && onToggle}>
      <Flex
        py={2}
        as={NextLink}
        href={href ?? '#'}
        justify={'space-between'}
        align={'center'}
        _hover={{
          textDecoration: 'none',
        }}>
        <Text
          fontWeight={600}
          color={useColorModeValue('gray.600', 'gray.200')}>
          {label}
        </Text>
        {children && (
          <Icon
            as={ChevronDownIcon}
            transition={'all .25s ease-in-out'}
            transform={isOpen ? 'rotate(180deg)' : ''}
            w={6}
            h={6}
          />
        )}
      </Flex>

      <Collapse in={isOpen} animateOpacity style={{ marginTop: '0!important' }}>
        <Stack
          mt={2}
          pl={4}
          borderLeft={1}
          borderStyle={'solid'}
          borderColor={useColorModeValue('gray.200', 'gray.700')}
          align={'start'}>
          {children &&
            children.map((child) => (
              <NextLink key={child.label} href={child.href ?? '#'} passHref>
                <Link py={2}>{child.label}</Link>
              </NextLink>
            ))}
        </Stack>
      </Collapse>
    </Stack>
  );
};

export default Navbar;