import ky from "ky";
import useSWR from "swr";
import { z } from "zod";

// parameters not implemented
const settings = {};
const game = "coi";

interface FetcherArgs {
  url: string;
  body: unknown;
}
export const fetcher = ({ url, body }: FetcherArgs) =>
  ky.post(url, { json: body }).json();

export function useItems(): string[] {
  const { data, error } = useSWR(
    { url: "/api/items", body: { settings, game } },
    fetcher,
  );
  if (error) {
    throw error;
  }
  return (data as string[]) ?? [];
}

export interface CalculatorInput {
  chosenRecipes: {
    input: Record<string, string>;
    byproduct: Record<string, string>;
  };
  outputItems: Array<{
    item: string;
    amount: number;
  }>;
}

const ItemAndAmountSchema = z.object({
  amount: z.number(),
  item: z.string(),
});

const RecipeSchema = z.object({
  inputs: z.array(ItemAndAmountSchema),
  outputs: z.array(ItemAndAmountSchema),
  machine: z.string(),
  duration: z.number(),
  id: z.string(),
});

const GraphSchema = z.object({
  edges: z.array(
    z.object({
      label: z.string(),
      source: z.string(),
      target: z.string(),
    }),
  ),
  nodes: z.array(
    z.discriminatedUnion("type", [
      z.object({
        type: z.enum(["input", "byproduct", "output", "input-end", "byproduct-end"]),
        color: z.string(),
        x: z.number(),
        y: z.number(),
        id: z.string(),
        labelInfo: ItemAndAmountSchema.extend({
          unit: z.string(),
        }),
      }),
      z.object({
        type: z.literal("recipe"),
        color: z.string(),
        x: z.number(),
        y: z.number(),
        id: z.string(),
        labelInfo: RecipeSchema.extend({
          quantity: z.number(),
        }),
      }),
    ]),
  ),
});
export type ApiGraph = z.infer<typeof GraphSchema>;

const CalculatorOutputSchema = z.object({
  graph: GraphSchema,
  requirements: z.array(
    z.object({ requirement: z.string(), value: z.number(), unit: z.string() }),
  ),
});
export type CalculatorOutput = z.infer<typeof CalculatorOutputSchema>;

export function useCalculator(
  input: CalculatorInput,
): CalculatorOutput | undefined {
  const { data, error } = useSWR(
    { url: "/api/calc", body: { ...input, settings, game } },
    fetcher,
  );
  if (error) {
    throw error;
  }

  if (!data) {
    return undefined;
  }
  return CalculatorOutputSchema.parse(data);
}

const RecipeOutputSchema = z.array(RecipeSchema);

export type RecipeOutput = z.infer<typeof RecipeOutputSchema>;

export interface RecipeInput {
  item: string;
  nodeType: "byproduct" | "input";
}

export function useRecipe(input: RecipeInput): RecipeOutput | undefined {
  const { data, error } = useSWR(
    { url: "/api/recipes", body: { ...input, settings, game } },
    fetcher,
  );
  if (error) {
    throw error;
  }

  if (!data) {
    return undefined;
  }
  return RecipeOutputSchema.parse(data);
}
