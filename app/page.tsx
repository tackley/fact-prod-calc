"use client";
import { Box } from "@mui/material";
import { ItemSelect } from "./_components/ItemSelect";
import { useState } from "react";
import { useCalculator } from "./_backend/hooks";

export default function Home() {
  const [item, setItem] = useState<string>();
  const graph = useCalculator({
    outputItems: item
      ? [
          {
            item,
            amount: 3,
          },
        ]
      : [],
    chosenRecipes: {
      consuming: {},
      producing: { Ammonia: "21" },
    },
  });

  return (
    <Box>
      <ItemSelect item={item} setItem={setItem} />

      <pre>{JSON.stringify(graph, undefined, 2)}</pre>
    </Box>
  );
}
