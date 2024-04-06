import "./App.css";
import { Button } from "@/components/ui/button";
import InputFile from "./components/inputs/InputFile";

function App() {
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
          <Button>Submit</Button>
        </div>
      </div>
    </div>
  );
}

export default App;
