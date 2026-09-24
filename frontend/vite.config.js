import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The browser only talks to this dev server. It forwards API calls to the Flask backend.
const BACKEND = "http://localhost:5000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: true,
    proxy: {
      "/chat": BACKEND,
      "/health": BACKEND,
    },
  },
});
