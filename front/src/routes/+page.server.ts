import type { PageServerLoad } from "./$types";
import { env } from "$env/dynamic/private";

export const load: PageServerLoad = async function ({ fetch }) {
    const url = new URL("/api/items/", env.API_URL);

    return {
        items: await (await fetch(url)).json(),
    };
};
