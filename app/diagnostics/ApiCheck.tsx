"use client";

import { Typography, Box, TextField } from "@mui/material";
import { ChangeEvent, useState } from "react";
import useSWR from "swr";
import { fetcher } from "../_backend/hooks";

interface Props {
  path: string;
  defaultInput: object;
}

function safeParse(s: string): object | undefined {
  try {
    return JSON.parse(s);
  } catch (e: any) {
    return undefined;
  }
}

export function ApiCheck({ path, defaultInput }: Props) {
  const [input, setInput] = useState(defaultInput);
  const [inputString, setInputString] = useState(
    JSON.stringify(defaultInput, undefined, 2),
  );
  const [parseError, setParseError] = useState<string>();

  const { data, error, isLoading } = useSWR(
    { url: path, body: input },
    fetcher,
  );

  const outputValue = parseError
    ? parseError
    : isLoading
      ? "Loading..."
      : error
        ? error.message
        : JSON.stringify(data, undefined, 2);

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const asJson = safeParse(e.target.value);

    if (asJson) {
      setInput(asJson);
      setInputString(JSON.stringify(asJson, undefined, 2));
      setParseError(undefined);
    } else {
      setInputString(e.target.value);
      setParseError("Invalid json");
    }
  };

  return (
    <Box>
      <Typography variant="h6">{path}</Typography>

      <TextField
        label="Input"
        multiline
        variant="outlined"
        value={inputString}
        fullWidth
        onChange={changeHandler}
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
