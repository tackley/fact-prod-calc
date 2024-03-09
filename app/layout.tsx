import { AppRouterCacheProvider } from "@mui/material-nextjs/v14-appRouter";
import { ThemeProvider } from "@mui/material/styles";
import { theme } from "@/theme";
import { Box, CssBaseline, Typography } from "@mui/material";
import { Satisfy } from "next/font/google";

const font = Satisfy({
  subsets: ["latin"],
  display: "swap",
  weight: ["400"],
});

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
              <Typography
                variant="h2"
                sx={{ mb: 2 }}
                fontFamily={font.style.fontFamily}
              >
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
