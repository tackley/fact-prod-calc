import { Typography } from "@mui/material";
import { NodeDisplay } from "./NodeDisplay";
import { ApiGraph } from "../_backend/hooks";
import { Dispatch } from "react";
import { SelectRecipeArgs } from "../page";

interface Props {
  graph: ApiGraph;
  onSelectRecipe: Dispatch<SelectRecipeArgs>;
}
export function TextCalcDisplay({ graph, onSelectRecipe }: Props) {
  const nodes = graph.nodes;

  const handleRecipeSelect =
    (type: "producing" | "consuming") =>
    (recipe: { item: string; id: string }) =>
      onSelectRecipe({ type, recipe });

  return (
    <>
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
    </>
  );
}
