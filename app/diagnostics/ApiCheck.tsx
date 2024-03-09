"use client";

import { Typography, Box, TextField } from "@mui/material";
import { useState } from "react";
import useSWR from "swr";
import { fetcher } from "../_backend/hooks";

interface Props {
  path: string;
  defaultInput: object;
}

export function ApiCheck({ path, defaultInput }: Props) {
  const [input, setInput] = useState(
    JSON.stringify(defaultInput, undefined, 2),
  );

  const { data, error, isLoading } = useSWR(
    { url: path, body: JSON.parse(input) },
    fetcher,
  );

  const outputValue = isLoading
    ? "Loading..."
    : error
      ? error.message
      : JSON.stringify(data, undefined, 2);

  return (
    <Box>
      <Typography variant="h6">{path}</Typography>

      <TextField
        label="Input"
        multiline
        variant="outlined"
        value={input}
        fullWidth
        onChange={(e) => setInput(e.target.value)}
        minRows={8}
        maxRows={8}
        sx={{ marginY: 1 }}
      />

      <TextField
        label="Output"
        multiline
        variant="outlined"
        value={outputValue}
        fullWidth
        minRows={8}
        maxRows={8}
        InputProps={{
          readOnly: true,
        }}
        sx={{ marginY: 1 }}
      />
    </Box>
  );
}
