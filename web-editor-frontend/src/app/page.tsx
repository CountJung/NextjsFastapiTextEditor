'use client';

import { AppBar, Box, Container, Toolbar, Typography } from '@mui/material';

import { ThemeModeToggle } from '@/components/ThemeModeToggle';
import { UploadConvert } from '@/components/UploadConvert';

export default function HomePage() {
  return (
    <Box sx={{ minHeight: '100vh' }}>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <Typography variant="h6" sx={{ flex: 1 }}>
            NextjsFastapiTextEditor
          </Typography>
          <ThemeModeToggle />
        </Toolbar>
      </AppBar>

      <Container sx={{ py: 3 }} maxWidth="lg">
        <UploadConvert />
      </Container>
    </Box>
  );
}
