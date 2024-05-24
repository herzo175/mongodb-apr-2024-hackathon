import { migrate } from "drizzle-orm/postgres-js/migrator";
import { conn, db } from "./server/db";
// import { migrate } from 'drizzle-orm/mysql2/migrator';
// import { db, connection } from './db';

// This will run migrations on the database, skipping the ones already applied
await migrate(db, { migrationsFolder: "./migrations" });
// Don't forget to close the connection, otherwise the script will hang
await conn.end();
