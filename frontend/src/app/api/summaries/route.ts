import { NextResponse } from "next/server";
import { db } from "~/server/db";
import { summaries } from "~/server/db/schema";
import { getServerSideClient } from "~/server/supabase";

export const POST = async () => {
  const createdSummaries = await db
    .insert(summaries)
    .values({ status: "AWAITING_UPLOAD" })
    .returning();

  if (!createdSummaries[0]) {
    return NextResponse.json(
      { error: "Failed to create summary" },
      { status: 500 },
    );
  }

  const { data, error } = await getServerSideClient()
    .storage.from("uploaded-videos")
    .createSignedUploadUrl(`${createdSummaries[0].id}.input.mp4`);

  if (error) {
    console.error("Error uploading file:", error);
    return NextResponse.json(
      { error: "Failed to upload file" },
      { status: 500 },
    );
  }

  return NextResponse.json({
    id: createdSummaries[0].id,
    status: createdSummaries[0].status,
    path: data.path,
    token: data.token,
  });
};
