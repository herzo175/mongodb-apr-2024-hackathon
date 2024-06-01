import { Connection } from "rabbitmq-client";
import { env } from "~/env";

// Initialize:
// TODO: double check if can build
const rabbit = new Connection(
  `amqp://${env.QUEUE_USER}:${env.QUEUE_PASS}@${env.QUEUE_HOST}:5672`,
);

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
