import { z } from "zod";

export const CreateSummaryResponseSchema = z.object({
  id: z.string(),
  status: z.string(),
  path: z.string(),
  token: z.string(),
});

export type CreateSummaryResponse = z.infer<typeof CreateSummaryResponseSchema>;

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
