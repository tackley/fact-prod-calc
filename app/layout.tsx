import { AppRouterCacheProvider } from "@mui/material-nextjs/v14-appRouter";
import { ThemeProvider } from "@mui/material/styles";
import { theme } from "@/theme";
import { Box, CssBaseline, Typography } from "@mui/material";

export const metadata = {
  title: "Fact! Prod! Calc!",
  description: "Factories. Production. Calculations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AppRouterCacheProvider>
            <Box padding={2}>
              <Typography variant="h1">
                Factory! Production! Calculator!
              </Typography>

              {children}
            </Box>
          </AppRouterCacheProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
