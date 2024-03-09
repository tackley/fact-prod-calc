"use client";
import { Box, Typography } from "@mui/material";
import { ItemSelect } from "./_components/ItemSelect";
import { useState } from "react";
import { CalculatorInput, useCalculator } from "./_backend/hooks";
import { NodeDisplay } from "./_components/NodeDisplay";

export default function Home() {
  const [input, setInput] = useState<CalculatorInput>({
    outputItems: [],
    chosenRecipes: {
      producing: {},
      consuming: {},
    },
  });

  const graph = useCalculator(input);

  const handleAddItem = (item: string) => {
    setInput((current) => ({
      ...current,
      outputItems: [
        ...current.outputItems,
        {
          item: item,
          amount: 1,
        },
      ],
    }));
  };

  const handleRecipeSelect =
    (type: "producing" | "consuming") =>
    (recipe: { item: string; id: string }) => {
      setInput((current) => ({
        ...current,
        chosenRecipes: {
          ...current.chosenRecipes,
          [type]: {
            ...current.chosenRecipes[type],
            [recipe.item]: recipe.id,
          },
        },
      }));
    };
  const nodes = graph?.graph.nodes ?? [];

  return (
    <Box>
      <Box display="flex" flexDirection="column" gap={1} maxWidth="250px">
        {input.outputItems.map((i) => (
          <ItemSelect
            key={i.item}
            item={i.item}
            setItem={() => alert("sorry can't change items yet!")}
          />
        ))}
        <ItemSelect add item={undefined} setItem={handleAddItem} />
      </Box>

      <Typography variant="h4" marginTop={2}>
        Inputs
      </Typography>

      {nodes
        .filter((n) => n.type === "input")
        .map((node) => (
          <NodeDisplay
            key={node.id}
            node={node}
            onRecipeSelect={handleRecipeSelect("producing")}
          />
        ))}

      <Typography variant="h4" marginTop={2}>
        Byproducts
      </Typography>

      {nodes
        .filter((n) => n.type === "byproduct")
        .map((node) => (
          <NodeDisplay
            key={node.id}
            node={node}
            onRecipeSelect={handleRecipeSelect("consuming")}
          />
        ))}

      <pre>{JSON.stringify(graph, undefined, 2)}</pre>
    </Box>
  );
}
