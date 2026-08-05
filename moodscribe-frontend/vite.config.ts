import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev proxy: forward API calls to the Flask backend on :5000 so the
// React app and the inference API share an origin during development.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/analyze": "http://localhost:5000",
      "/get_messages": "http://localhost:5000",
      "/login": "http://localhost:5000",
      "/set_thread": "http://localhost:5000",
    },
  },
});
