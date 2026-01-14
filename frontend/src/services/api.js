import axios from "axios";
import { API_BASE_URL } from "../constants/env";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 20000,
});

export async function sendChatMessage({ userId, message }) {
  const payload = { user_id: userId, message };
  const { data } = await apiClient.post("/chat/message", payload);
  return data;
}
