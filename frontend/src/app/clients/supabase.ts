import { env } from "~/env";
import { createBrowserClient } from "@supabase/ssr";

export const getBrowserClient = () => {
  return createBrowserClient(
    env.NEXT_PUBLIC_SUPABASE_URL,
    env.NEXT_PUBLIC_SUPABASE_PUBLIC_KEY,
  );
};
