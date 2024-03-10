import { Dispatch } from "react";
import { SelectRecipeArgs } from "../page";
import { ApiGraph } from "../_backend/hooks";
import "@react-sigma/core/lib/react-sigma.min.css";
import { convertApiResponseToGraph } from "../_utils/graph";

import { useEffect } from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/react-sigma.min.css";

export const LoadGraph = (props: { apiGraph: ApiGraph }) => {
  const loadGraph = useLoadGraph();

  useEffect(() => {
    const graph = convertApiResponseToGraph(props.apiGraph);
    graph.addNode("first", {
      x: 0,
      y: 0,
      size: 15,
      label: "My first node",
      color: "#FA4F40",
    });
    loadGraph(graph);
  }, [loadGraph, props.apiGraph]);

  return null;
};

interface Props {
  graph: ApiGraph;
  onSelectRecipe: Dispatch<SelectRecipeArgs>;
}

export function GraphCalcDisplay({ graph, onSelectRecipe }: Props) {
  const g = convertApiResponseToGraph(graph);

  return (
    <SigmaContainer style={{ height: "500px", width: "500px" }}>
      <LoadGraph apiGraph={graph} />
    </SigmaContainer>
  );
}
