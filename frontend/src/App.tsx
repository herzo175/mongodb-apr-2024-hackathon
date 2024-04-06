import { useNavigate } from "react-router-dom";
import "./App.css";
import InputFile from "./components/inputs/InputFile";
import { Button } from "./components/ui/button";

function App() {
  const navigate = useNavigate();

  const uploadFile = () => {
    navigate("/summary");
  };

  return (
    <div className="flex flex-col items-center space-y-8">
      <div className="space-y-2">
        <h1 className="text-6xl">TikTokify!</h1>
        <h2 className="text-3xl">Upload a video to turn it into a short</h2>
      </div>
      <div className="flex flex-col items-center space-y-4">
        <div>
          <InputFile />
        </div>

        <div>
          <Button onClick={uploadFile}>Submit</Button>
        </div>
      </div>
    </div>
  );
}

export default App;
