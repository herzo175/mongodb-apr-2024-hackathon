import { eq } from "drizzle-orm";
import { NextRequest, NextResponse } from "next/server";
import { UpdateStatusSchema } from "~/models/summaries";
import { db } from "~/server/db";
import { summaries } from "~/server/db/schema";
import { tasksQueuePub } from "~/server/rabbitmq";
import { getServerSideClient } from "~/server/supabase";

export const dynamic = "force-dynamic"; // defaults to auto

export const GET = async (
  request: Request,
  { params }: { params: { videoId: string } },
) => {
  const videoSummaries = await db
    .select()
    .from(summaries)
    .where(eq(summaries.id, params.videoId));

  if (!videoSummaries[0]) {
    return Response.json({ error: "Video Summary Not Found" }, { status: 404 });
  }

  const videoSummary = videoSummaries[0];
  let url: string | null = null;

  if ("FINISHED" == videoSummary.status) {
    const { data, error } = await getServerSideClient()
      .storage.from("processed-videos")
      .createSignedUrl(`${params.videoId}.output.mp4`, 60);

    if (error) {
      return Response.json(
        { error: "Couldn't Get Video Presigned URL" },
        { status: 500 },
      );
    }

    url = data.signedUrl;
  }

  return Response.json({
    id: videoSummary.id,
    status: videoSummary.status,
    url,
  });
};

export const POST = async (
  request: Request,
  { params }: { params: { videoId: string } },
) => {
  await tasksQueuePub.send(
    "tasks",
    JSON.stringify({
      video_id: params.videoId,
    }),
  );

  return NextResponse.json({ submitted: true });
};

export const PUT = async (
  request: Request,
  { params }: { params: { videoId: string } },
) => {
  const { status } = UpdateStatusSchema.parse(await request.json());

  const updated = await db
    .update(summaries)
    .set({ status })
    .where(eq(summaries.id, params.videoId))
    .returning();

  if (!updated[0]) {
    return Response.json({ error: "Failed to update status" }, { status: 500 });
  }

  const channel = getServerSideClient().channel(params.videoId);

  await channel.send({
    type: "broadcast",
    event: "message",
    payload: { status },
  });

  return Response.json({
    id: updated[0].id,
    status: updated[0].status,
  });
};
