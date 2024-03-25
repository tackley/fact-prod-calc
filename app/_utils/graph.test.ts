import { expect, it } from "vitest";
import { convertApiResponseToGraph } from "./graph";
import { ApiGraph } from "../_backend/hooks";

it("should convert a simple graph", () => {
  const input: ApiGraph = {
    edges: [
      {
        details: {
          amount: 1,
          item: "Iron ore",
          unit: "/min",
        },
        end: "1",
        start: "0",
      },
    ],
    nodes: [
      {
        type: "input",
        details: {
          amount: 1,
          item: "Iron ore",
          unit: "/min",
        },
        id: "0",
      },
      {
        type: "output",
        details: {
          amount: 1,
          item: "Iron ore",
          unit: "/min",
        },
        id: "1",
      },
    ],
  };

  const result = convertApiResponseToGraph(input);

  expect(result.edges()).toHaveLength(1);

  expect(result.nodes()).toHaveLength(2);

  expect(result.inspect()).toMatchInlineSnapshot(`
    Graph {
      "allowSelfLoops": true,
      "attributes": {},
      "directedSelfLoopCount": 0,
      "directedSize": 1,
      "edges": {
        "(0)->(1)": {
          "label": "1/min Iron ore",
          "size": 4,
          "type": "arrow",
        },
      },
      "implementation": "graphology",
      "multi": false,
      "nodes": {
        "0": {
          "color": "#FFC080",
          "label": "Iron ore",
          "nodeType": "input",
          "size": 15,
          "x": 100,
          "y": 10,
        },
        "1": {
          "color": "#80FFC0",
          "label": "Iron ore",
          "nodeType": "output",
          "size": 15,
          "x": 200,
          "y": 20,
        },
      },
      "order": 2,
      "selfLoopCount": 0,
      "size": 1,
      "type": "directed",
      "undirectedSelfLoopCount": 0,
      "undirectedSize": 0,
    }
  `);
});
