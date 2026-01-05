//apis.js
import axios from "axios";

// [TODO]: Update with Gawon's LLM server
// const baseURL = "http://localhost:3001/api";
const baseURL = "https://cyberbullying-tuned.onrender.com/api";
const instance = axios.create({
  baseURL: baseURL,
});

export const getLLMResponse = (data) => {
  return instance.post(`/getLLMResponse`, data);
};
