import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import EventsPage from "./pages/EventsPage";
import EventDetailPage from "./pages/EventDetailPage";

function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/" element={<EventsPage />} />
        <Route path="/events/:id" element={<EventDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;