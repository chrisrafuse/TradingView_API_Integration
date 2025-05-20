// App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Webhooks from "./pages/Webhooks";
import Nav from "./components/Nav";
import Orders from "./pages/Orders";
import Positions from "./pages/Positions";
import Profits from "./pages/Profits"

function App() {
  return (
    <div className="bg-gray-100 min-h-screen">
    <BrowserRouter>
      <Nav />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/webhooks" element={<Webhooks />} />
          <Route path="/positions" element={<Positions />} />
          <Route path="/profits" element={<Profits />} />
        </Routes>      
    </BrowserRouter>
    </div>
  );
}

export default App;
