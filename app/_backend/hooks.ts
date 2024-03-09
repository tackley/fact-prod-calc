import ky from "ky";
import useSWR from "swr";

// parameters not implemented
const settings = {};
const game = "coi";
const postData = {
  settings: settings,
  game: game,
};

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

interface CalculatorInput {
  chosenRecipes: {
    producing: Record<string, string>;
    consuming: Record<string, string>;
  };
  outputItems: Array<{
    item: string;
    amount: number;
  }>;
  settings: Record<string, any>;
  game: "coi";
}

type CalculatorOutput = any;

export function useCalculator(
  input: Omit<CalculatorInput, "settings" | "game">,
): CalculatorOutput | undefined {
  const { data, error } = useSWR(
    { url: "/api/calc", body: { ...input, settings, game } },
    fetcher,
  );
  if (error) {
    throw error;
  }
  return data;
}
