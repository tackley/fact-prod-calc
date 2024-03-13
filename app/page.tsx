"use client";
import { Box, Tab, Tabs, Typography } from "@mui/material";
import { ItemSelect } from "./_components/ItemSelect";
import { useState } from "react";
import { CalculatorInput, useCalculator } from "./_backend/hooks";
import { NodeDisplay } from "./_components/NodeDisplay";
import { TextCalcDisplay } from "./_components/TextCalcDisplay";
import { GraphCalcDisplay } from "./_components/GraphCalcDisplay";

export interface SelectRecipeArgs {
  type: "producing" | "consuming";
  recipe: { item: string; id: string };
}

export default function Home() {
  const [input, setInput] = useState<CalculatorInput>({
    outputItems: [],
    chosenRecipes: {
      producing: {},
      consuming: {},
    },
  });
  const [selectedTab, setSelectedTab] = useState(0);

  const calcResult = useCalculator(input);
  const graph = calcResult?.graph;

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

  const handleSelectRecipe = ({ type, recipe }: SelectRecipeArgs) => {
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
  const nodes = calcResult?.graph.nodes ?? [];

  return (
    <Box>
      <Box display="flex" flexDirection="column" gap={1} maxWidth="400px">
        {input.outputItems.map((i) => (
          <ItemSelect
            key={i.item}
            item={i.item}
            setItem={() => alert("sorry can't change items yet!")}
          />
        ))}
        <ItemSelect add item={undefined} setItem={handleAddItem} />
      </Box>

      <Tabs
        value={selectedTab}
        onChange={(e, newValue) => setSelectedTab(newValue)}
      >
        <Tab label="Text" />
        <Tab label="Graph" />
        <Tab label="Debug" />
      </Tabs>

      {selectedTab === 0 && graph && (
        <TextCalcDisplay graph={graph} onSelectRecipe={handleSelectRecipe} />
      )}

      {selectedTab === 1 && graph && (
        <GraphCalcDisplay graph={graph} onSelectRecipe={handleSelectRecipe} />
      )}

      {selectedTab === 2 && (
        <pre>{JSON.stringify(calcResult, undefined, 2)}</pre>
      )}
    </Box>
  );
}
