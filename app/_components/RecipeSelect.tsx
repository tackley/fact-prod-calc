import {
  Button,
  Dialog,
  DialogTitle,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import { RecipeInput, RecipeOutput, useRecipe } from "../_backend/hooks";
import { Dispatch, useState } from "react";

interface Props {
  input: RecipeInput;
  onSelect: Dispatch<{ item: string; id: string }>;
}

function formatRecipe(r: RecipeOutput[0]): string {
  const inputs = r.inputs.map((i) => `${i.amount} ${i.item}`).join(", ");
  const outputs = r.outputs.map((o) => `${o.amount} ${o.item}`).join(", ");
  const duration = r.duration;
  return `${inputs} → ${outputs} in ${duration}s`;
}

export function RecipeSelect({ input, onSelect }: Props) {
  const [open, setOpen] = useState(false);
  const result = useRecipe(input);

  const handleClose = () => setOpen(false);
  const handleOpen = () => setOpen(true);
  return (
    <>
      <Button
        variant="text"
        size="small"
        disabled={!result}
        onClick={handleOpen}
      >
        Select&nbsp;Recipe
      </Button>
      <Dialog onClose={handleClose} open={open}>
        <DialogTitle>Choose Recipe</DialogTitle>
        <List dense sx={{ paddingTop: 0 }}>
          {result?.map((r) => (
            <ListItem disableGutters key={r.id}>
              <ListItemButton
                onClick={() => onSelect({ item: input.item, id: r.id })}
              >
                <ListItemText primary={r.machine} secondary={formatRecipe(r)} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Dialog>
    </>
  );
}
