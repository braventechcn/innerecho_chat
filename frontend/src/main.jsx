import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import { GlobalStyles } from "./styles/globalStyles.js";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <React.StrictMode>
    <GlobalStyles />
    <App />
  </React.StrictMode>
);
