import { Box, Container, Typography } from "@mui/material";
import { ApiCheck } from "./ApiCheck";

export default function Diagnostics() {
  return (
    <>
      <Typography variant="h2" gutterBottom>
        Diagnostics Page
      </Typography>

      <Box display="grid" gridTemplateColumns="repeat(4, 1fr)" gap={2}>
        <ApiCheck
          path="/api/items"
          defaultInput={{ settings: {}, game: "coi" }}
        />
        <ApiCheck
          path="/api/recipes"
          defaultInput={{
            settings: {},
            game: "coi",
            item: "Acid",
            nodeType: "input",
          }}
        />
        <ApiCheck
          path="/api/calc"
          defaultInput={{
            settings: {},
            game: "coi",
            chosenRecipes: {
              producing: {},
              consuming: {},
            },
            outputItems: [
              {
                item: "Acid",
                amount: 5,
              },
            ],
          }}
        />
        <ApiCheck path="/api/settings" defaultInput={{ game: "coi" }} />
      </Box>
    </>
  );
}
