import { Dispatch, useState } from "react";
import { SelectRecipeArgs } from "../page";
import { ApiGraph, RecipeInput } from "../_backend/hooks";
import "@react-sigma/core/lib/react-sigma.min.css";
import { convertApiResponseToGraph } from "../_utils/graph";

import { useEffect } from "react";
import Graph from "graphology";
import {
  ControlsContainer,
  SigmaContainer,
  useLoadGraph,
  useRegisterEvents,
} from "@react-sigma/core";
import "@react-sigma/core/lib/react-sigma.min.css";
import { RecipeMenu } from "./RecipeSelect";
import forceAtlas2 from "graphology-layout-forceatlas2";

interface Props {
  graph: ApiGraph;
  onSelectRecipe: Dispatch<SelectRecipeArgs>;
}

function GraphEvents({
  graph,
  onSelectRecipe,
}: {
  graph: Graph;
  onSelectRecipe: Dispatch<SelectRecipeArgs>;
}) {
  const registerEvents = useRegisterEvents();
  const [item, setItem] = useState<RecipeInput>();

  useEffect(() => {
    // Register the events
    registerEvents({
      // node events
      clickNode: (event) => {
        const theNode = graph.getNodeAttributes(event.node);
        setItem({ item: theNode.label, nodeType: theNode.nodeType });
      },
    });
  }, [registerEvents]);

  const handleClose = () => {
    setItem(undefined);
  };

  if (item) {
    return (
      <RecipeMenu
        input={item}
        open
        onClose={handleClose}
        onSelect={(recipe) => {
          onSelectRecipe({
            type: item.nodeType === "byproduct" ? "consuming" : "producing",
            recipe,
          });
          handleClose();
        }}
      />
    );
  }

  return null;
}

/*
const ForceAtlas2Layout: React.FC = () => {
  const { start, kill, isRunning } = useWorkerLayoutForceAtlas2({
    settings: { barnesHutOptimize: true },
  });

  useEffect(() => {
    start();
    return () => {
      kill();
    };
  }, [start, kill]);

  return null;
};
*/

export function GraphCalcDisplay({ graph: apiGraph, onSelectRecipe }: Props) {
  const graph = convertApiResponseToGraph(apiGraph);
  const settings = forceAtlas2.inferSettings(graph);
  forceAtlas2.assign(graph, { iterations: 50, settings });

  return (
    <SigmaContainer
      style={{ height: "500px", width: "100%" }}
      graph={graph}
      settings={{ renderEdgeLabels: true }}
    >
      <GraphEvents graph={graph} onSelectRecipe={onSelectRecipe} />
    </SigmaContainer>
  );
}
