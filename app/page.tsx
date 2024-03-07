"use client";
import { Box, Button, Typography } from "@mui/material";

export default function Home() {
  return (
    <Box padding={2}>
      <Typography variant="h1">Hello?</Typography>
      <Button variant="contained" onClick={() => alert("Goodbye!")}>
        Press Me
      </Button>
    </Box>
  );
}
