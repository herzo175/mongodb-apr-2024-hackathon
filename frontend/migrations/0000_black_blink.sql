CREATE TABLE IF NOT EXISTS "showstopper_summaries" (
	"id" text PRIMARY KEY NOT NULL,
	"status" text,
	"created_at" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	"updated_at" timestamp
);
