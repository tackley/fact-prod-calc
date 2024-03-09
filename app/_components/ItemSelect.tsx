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
  add?: boolean;
  item: string | undefined;
  setItem: Dispatch<string>;
}

export function ItemSelect({ item, setItem, add }: Props) {
  const items = useItems();

  const handleChange = (event: SelectChangeEvent) => {
    setItem(event.target.value as string);
  };

  return (
    <FormControl variant="filled" sx={{ minWidth: 200 }}>
      <InputLabel id="item-label">
        {add ? "Add Item" : "Change Item"}
      </InputLabel>
      <Select labelId="item-label" value={item ?? ""} onChange={handleChange}>
        {items.map((i) => (
          <MenuItem key={i} value={i}>
            {i}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
