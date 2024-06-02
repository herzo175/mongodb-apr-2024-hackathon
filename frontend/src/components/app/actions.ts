import { CreateSummaryResponseSchema } from "~/models/summaries";

export const makeVideoUploadURL = async () => {
  const response = await fetch("/api/summaries", {
    method: "POST",
  });

  return CreateSummaryResponseSchema.parse(await response.json());
};

export const submitProcessingJob = async (videoId: string) => {
  await fetch(`/api/summaries/${videoId}`, {
    method: "POST",
  });

  return;
};
