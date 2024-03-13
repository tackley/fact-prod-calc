import Graph from "graphology";
import { ApiGraph } from "../_backend/hooks";

const fmt = new Intl.NumberFormat(undefined, { maximumFractionDigits: 2 });

const typeColours = {
  input: "#FFC080",
  byproduct: "#FFC080",
  output: "#80FFC0",
  recipe: "#80C0FF",
};

export function convertApiResponseToGraph(api: ApiGraph): Graph {
  const g = new Graph({ type: "directed" });
  let posIndex = 0;
  for (const node of api.nodes) {
    posIndex += 1;

    let label;
    if (node.type === "recipe") {
      label = node.details.machine;
    } else {
      label = node.details.item;
    }
    g.addNode(node.id, {
      label,
      nodeType: node.type,
      size: 15,
      color: typeColours[node.type],
      x: (posIndex % 10) * 100,
      y: posIndex * 10,
    });
  }

  for (const edge of api.edges) {
    g.addEdge(edge.start, edge.end, {
      label: `${fmt.format(edge.details.amount)}${edge.details.unit} ${edge.details.item}`,
      type: "arrow",
      size: 4,
    });
  }

  console.log(g);

  return g;
}
