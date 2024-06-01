import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

import * as schema from "./schema";
import { dbEnv } from "~/dbEnv";

/**
 * Cache the database connection in development. This avoids creating a new connection on every HMR
 * update.
 */
const globalForDb = globalThis as unknown as {
  conn: postgres.Sql | undefined;
};

export const conn = globalForDb.conn ?? postgres(dbEnv.DATABASE_URL);
if (dbEnv.NODE_ENV !== "production") globalForDb.conn = conn;

export const db = drizzle(conn, { schema });
