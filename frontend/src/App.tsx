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
    <div className="flex flex-col items-center space-y-16">
      <div>
        <h1>Upload a video to turn it into a short:</h1>
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
