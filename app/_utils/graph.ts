import Graph from "graphology";
import { ApiGraph } from "../_backend/hooks";

export function convertApiResponseToGraph(api: ApiGraph): Graph {
  const g = new Graph({ type: "directed" });

  for (const node of api.nodes) {
    g.addNode(node.id, {
      ...node,
      x: 0,
      y: 0,
    });
  }

  for (const edge of api.edges) {
    g.addEdge(edge.start, edge.end, edge.details);
  }

  return g;
}
