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
          "amount": 1,
          "item": "Iron ore",
          "unit": "/min",
        },
      },
      "implementation": "graphology",
      "multi": false,
      "nodes": {
        "0": {
          "details": {
            "amount": 1,
            "item": "Iron ore",
            "unit": "/min",
          },
          "id": "0",
          "type": "input",
        },
        "1": {
          "details": {
            "amount": 1,
            "item": "Iron ore",
            "unit": "/min",
          },
          "id": "1",
          "type": "output",
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
