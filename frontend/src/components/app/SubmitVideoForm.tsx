"use client";

import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { makeVideoUploadURL, submitProcessingJob } from "./actions";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { getBrowserClient } from "~/app/clients/supabase";

const SubmitVideoForm = () => {
  const [videoFile, setVideoFile] = useState<File>();
  const [buttonText, setButtonText] = useState("Create Short");
  const [showSpinner, setShowSpinner] = useState(false);

  const router = useRouter();

  const handleSubmitVideo = async () => {
    if (!videoFile) {
      return;
    }

    setShowSpinner(true);

    const { id, path, token } = await makeVideoUploadURL();

    if (!id) {
      console.error("error submitting video");
      setShowSpinner(false);
      return;
    }

    setButtonText("Uploading Video");

    const { data: uploadData } = await getBrowserClient()
      .storage.from("uploaded-videos")
      .uploadToSignedUrl(path, token, videoFile);

    if (!uploadData) {
      setButtonText("Upload Failed!");
      setShowSpinner(false);
      return;
    }

    await submitProcessingJob(id);

    setButtonText("Processing Video");
    setShowSpinner(false);
    router.push(`/summaries/${id}`);
  };

  return (
    <div className="w-1/2 flex-col space-y-4 pt-8">
      <div className="w-full">
        <Input
          id="video"
          type="file"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              setVideoFile(e.target.files[0]);
            }
          }}
        />
      </div>

      {videoFile && (
        <div className="flex w-full">
          <Button className="w-full" size={"lg"} onClick={handleSubmitVideo}>
            {showSpinner ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <></>
            )}
            {buttonText}
          </Button>
        </div>
      )}
    </div>
  );
};

export default SubmitVideoForm;
