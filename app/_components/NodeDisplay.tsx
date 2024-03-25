import { Box, Button, Typography } from "@mui/material";
import { CalculatorOutput } from "../_backend/hooks";
import { RecipeButton } from "./RecipeSelect";
import { Dispatch } from "react";

type Node = CalculatorOutput["graph"]["nodes"][0];

interface Props {
  node: Node;
  onRecipeSelect: Dispatch<{ item: string; id: string }>;
}

export function NodeDisplay({ node, onRecipeSelect }: Props) {
  if (node.type === "recipe") {
    return <Typography>{node.labelInfo.machine}</Typography>;
  }
  if (node.type === "output" || node.type === "byproduct-end" || node.type == "input-end") {
    return (
      <Typography>
        {node.labelInfo.amount}{node.labelInfo.unit} {node.labelInfo.item}
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
          {node.labelInfo.amount}{node.labelInfo.unit} {node.labelInfo.item}
        </Typography>
        <RecipeButton
          input={{ item: node.labelInfo.item, nodeType: node.type }}
          onSelect={onRecipeSelect}
        />
      </Box>
    );
  }
}
