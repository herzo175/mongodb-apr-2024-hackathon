import { z } from "zod";

export const GetSummarySchema = z.object({
  id: z.string(),
  url: z.string().nullable(),
  status: z.string(),
});

export type GetSummary = z.infer<typeof GetSummarySchema>;

export const UpdateStatusSchema = z.object({
  status: z.string(),
});

export type UpdateStatus = z.infer<typeof UpdateStatusSchema>;
