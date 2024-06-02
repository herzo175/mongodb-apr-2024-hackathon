import { Connection } from "rabbitmq-client";
import { env } from "~/env";

// Initialize:
const rabbit = new Connection({
  hostname: env.QUEUE_HOST,
  username: env.QUEUE_USER,
  password: env.QUEUE_PASS,
});

rabbit.on("error", (err) => {
  console.log("RabbitMQ connection error", err);
});

rabbit.on("connection", () => {
  console.log("Connection successfully (re)established");
});

// Declare a publisher
// See API docs for all options
export const tasksQueuePub = rabbit.createPublisher({
  // Enable publish confirmations, similar to consumer acknowledgements
  confirm: true,
  // Enable retries
  maxAttempts: 2,
  exchanges: [{ exchange: "tasks" }],
});
