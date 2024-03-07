// src/theme.ts
"use client";
import { Raleway } from "next/font/google";
import { createTheme } from "@mui/material/styles";

const font = Raleway({
  subsets: ["latin"],
  display: "swap",
});

export const theme = createTheme({
  typography: {
    fontFamily: font.style.fontFamily,
  },
});
