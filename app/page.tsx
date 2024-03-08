"use client";
import { Box } from "@mui/material";
import { ItemSelect } from "./_components/ItemSelect";
import { useState } from "react";

export default function Home() {
  const [item, setItem] = useState<string>();

  return (
    <Box>
      <ItemSelect item={item} setItem={setItem} />
    </Box>
  );
}
