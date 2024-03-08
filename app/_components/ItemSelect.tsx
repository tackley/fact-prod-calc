import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from "@mui/material";
import { Dispatch } from "react";
import { useItems } from "../_backend/hooks";

interface Props {
  item: string | undefined;
  setItem: Dispatch<string>;
}

export function ItemSelect({ item, setItem }: Props) {
  const items = useItems();

  const handleChange = (event: SelectChangeEvent) => {
    setItem(event.target.value as string);
  };

  return (
    <FormControl variant="filled" sx={{ minWidth: 200 }}>
      <InputLabel id="item-label">Add Item</InputLabel>
      <Select
        labelId="item-label"
        value={item ?? ""}
        label="Please Add Item"
        onChange={handleChange}
      >
        {items.map((i) => (
          <MenuItem value={i}>{i}</MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
