import ky from "ky";
import useSWR from "swr";

const fetcher = (url: string) => ky(url).json();

export function useItems(): string[] {
  const { data, error } = useSWR("/api/items/coi", fetcher);
  if (error) {
    throw error;
  }
  console.log(data);
  return (data as string[]) ?? [];
}
