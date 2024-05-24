// Example model schema from the Drizzle docs
// https://orm.drizzle.team/docs/sql-schema-declaration

import { createId } from "@paralleldrive/cuid2";
import { sql } from "drizzle-orm";
import { pgTableCreator, text, timestamp } from "drizzle-orm/pg-core";

/**
 * This is an example of how to use the multi-project schema feature of Drizzle ORM. Use the same
 * database instance for multiple projects.
 *
 * @see https://orm.drizzle.team/docs/goodies#multi-project-schema
 */
export const createTable = pgTableCreator((name) => `showstopper_${name}`);

export const summaries = createTable("summaries", {
  id: text("id")
    .$defaultFn(() => createId())
    .primaryKey(),
  status: text("status"),
  createdAt: timestamp("created_at")
    .default(sql`CURRENT_TIMESTAMP`)
    .notNull(),
  updatedAt: timestamp("updated_at"),
});
