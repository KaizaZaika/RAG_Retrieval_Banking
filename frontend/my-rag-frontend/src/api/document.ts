import { api } from "./client";

export async function uploadDocument(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/documents/upload",
    formData
  );

  return response.data;
}
