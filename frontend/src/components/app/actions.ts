"use server";

import { AMQPClient } from "@cloudamqp/amqp-client";
import { env } from "~/env";
import { db } from "~/server/db";
import { summaries } from "~/server/db/schema";
import { supabase } from "~/server/supabase";

export const makeVideoUploadURL = async (): Promise<
  | {
      error: null;
      data: { id: string; status: string | null; path: string; token: string };
    }
  | { error: string; data: null }
> => {
  const createdSummaries = await db
    .insert(summaries)
    .values({ status: "AWAITING_UPLOAD" })
    .returning();

  if (!createdSummaries[0]) {
    return { error: "Failed to create summary", data: null };
  }

  const { data, error } = await supabase.storage
    .from("uploaded-videos")
    .createSignedUploadUrl(`${createdSummaries[0].id}.input.mp4`);

  if (error) {
    console.error("Error uploading file:", error);
    return { error: "Failed to upload file", data: null };
  }

  return {
    error: null,
    data: {
      id: createdSummaries[0].id,
      status: createdSummaries[0].status,
      path: data.path,
      token: data.token,
    },
  };
};

export const submitProcessingJob = async (videoId: string) => {
  const amqp = new AMQPClient(env.QUEUE_URL);
  const conn = await amqp.connect();
  try {
    const ch = await conn.channel();
    const q = await ch.queue("tasks");
    await q.publish(
      JSON.stringify({
        video_id: videoId,
      }),
      { deliveryMode: 2 },
    );
  } catch (e) {
    console.error("error submitting job:", e);
  } finally {
    await conn.close();
  }
};
