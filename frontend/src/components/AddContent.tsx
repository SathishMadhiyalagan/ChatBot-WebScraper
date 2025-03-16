import { useState } from "react";
import axios from "axios";

const AddContent = () => {
  const [activeTab, setActiveTab] = useState<"webScraping" | "addContent">("webScraping");
  const [content, setContent] = useState("");
  const [savedContent, setSavedContent] = useState<string[]>([]);

  // API URLs
  const WEB_SCRAPING_API = "http://127.0.0.1:8000/web/";
  const CONTENT_API = "http://127.0.0.1:8000/web/contentRag";

  // Web Scraping Function
  const handleWebScraping = async () => {
    try {
      const response = await axios.get(WEB_SCRAPING_API);
      alert("Web Scraping Started! 🚀");
      console.log("Web Scraping Response:", response.data);
    } catch (error) {
      console.error("Web Scraping Error:", error.response?.data || "Unknown error");
    }
  };

  // Save Content Function
  const handleSave = async () => {
    if (!content.trim()) return alert("Please enter content before saving!");

    try {
      const response = await axios.post(CONTENT_API, { text: content }, { 
        headers: { "Content-Type": "application/json" } 
      });

      setSavedContent([...savedContent, content]);
      setContent("");
      console.log("Content Saved Response:", response.data);
    } catch (error) {
      console.error("Error Saving Content:", error.response?.data || "Unknown error");
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 bg-white rounded-lg shadow-lg border">
      {/* Tab Navigation */}
      <div className="flex border-b mb-4">
        <button
          onClick={() => setActiveTab("webScraping")}
          className={`px-4 py-2 text-lg font-semibold border-b-2 transition ${
            activeTab === "webScraping"
              ? "border-blue-500 text-blue-500"
              : "border-transparent text-gray-500 hover:text-blue-500"
          }`}
        >
          Web Scraping
        </button>
        <button
          onClick={() => setActiveTab("addContent")}
          className={`px-4 py-2 text-lg font-semibold border-b-2 transition ${
            activeTab === "addContent"
              ? "border-blue-500 text-blue-500"
              : "border-transparent text-gray-500 hover:text-blue-500"
          }`}
        >
          Add Content
        </button>
      </div>

      {/* Web Scraping Section */}
      {activeTab === "webScraping" && (
        <div className="p-4 bg-gray-100 rounded-lg shadow-lg">
          <h2 className="text-xl font-bold mb-2">Web Scraping Page</h2>
          <p className="text-gray-600 mb-4">
            This page allows you to perform web scraping. Click the button below to scrape data from a website.
          </p>

          <button
            onClick={handleWebScraping}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          >
            Start Web Scraping
          </button>
        </div>
      )}

      {/* Add Content Section */}
      {activeTab === "addContent" && (
        <div className="p-4 bg-gray-100 rounded-lg shadow-lg mt-4">
          <h3 className="text-xl font-bold mb-2">Add Content</h3>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-2 border rounded mt-2"
            placeholder="Enter content..."
          ></textarea>
          <button
            onClick={handleSave}
            className="mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition"
          >
            Save
          </button>

          <div className="mt-4">
            <h3 className="font-semibold">Saved Content:</h3>
            {savedContent.map((item, index) => (
              <p key={index} className="p-2 bg-gray-200 rounded mt-1">{item}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AddContent;
