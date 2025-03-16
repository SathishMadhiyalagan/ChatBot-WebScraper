import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Chat from "./components/Chat";
import AddContent from "./components/AddContent"; // ✅ Import the AddContent component

function App() {
  return (
    <Router>
      <div className="p-4">
        {/* Navigation Bar */}
        <nav className="mb-4 flex gap-4">
          <Link to="/chat" className="text-blue-500 font-semibold">Chat</Link>
          <Link to="/addContent" className="text-blue-500 font-semibold">Add Content</Link> {/* ✅ Fixed the text */}
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/chat" element={<Chat />} />
          <Route path="/addContent" element={<AddContent />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
