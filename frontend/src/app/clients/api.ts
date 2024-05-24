export const fetchJSON = (url: string) => fetch(url).then((r) => r.json());
