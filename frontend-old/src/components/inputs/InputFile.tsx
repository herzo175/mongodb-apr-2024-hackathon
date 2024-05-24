import { Input } from "@/components/ui/input";

const InputFile = () => {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Input id="video" type="file" />
    </div>
  );
};

export default InputFile;
