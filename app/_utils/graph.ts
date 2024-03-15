import Graph from "graphology";
import { ApiGraph } from "../_backend/hooks";

export function convertApiResponseToGraph(api: ApiGraph): Graph {
  const g = new Graph({ type: "directed", multi: true});
  let posIndex = 0;
  for (const node of api.nodes) {
    posIndex += 1;

    let label;
    if (node.type === "recipe") {
      label = node.labelInfo.machine;
    } else {
      label = node.labelInfo.item;
    }
    g.addNode(node.id, {
      label,
      nodeType: node.type,
      size: 15,
      color: node.color,
      x: node.x,
      y: node.y,
    });
  }

  for (const edge of api.edges) {
    g.addEdge(edge.source, edge.target, {
      label: edge.label,
      type: "arrow",
      size: 4,
    });
  }

  console.log(g);

  return g;
}
