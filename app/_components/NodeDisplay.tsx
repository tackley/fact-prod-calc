import { Box, Button, Typography } from "@mui/material";
import { CalculatorOutput } from "../_backend/hooks";
import { RecipeSelect } from "./RecipeSelect";
import { Dispatch } from "react";

type Node = CalculatorOutput["graph"]["nodes"][0];

interface Props {
  node: Node;
  onRecipeSelect: Dispatch<{ item: string; id: string }>;
}

export function NodeDisplay({ node, onRecipeSelect }: Props) {
  if (node.type === "recipe") {
    return <Typography>{node.details.machine}</Typography>;
  }
  if (node.type === "output") {
    return (
      <Typography>
        {node.details.amount} per min {node.details.item}
      </Typography>
    );
  } else {
    return (
      <Box
        display="flex"
        alignItems="baseline"
        gap={1}
        justifyContent="space-between"
        maxWidth={400}
      >
        <Typography>
          {node.details.amount} per min {node.details.item}
        </Typography>
        <RecipeSelect
          input={{ item: node.details.item, nodeType: node.type }}
          onSelect={onRecipeSelect}
        />
      </Box>
    );
  }
}
