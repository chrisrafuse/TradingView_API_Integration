// main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx"; // make sure the path is correct
import "./index.css"; // or your CSS file

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
