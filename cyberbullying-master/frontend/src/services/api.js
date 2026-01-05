//apis.js
import axios from "axios";

const baseURL = "https://cyberbullying-g80i.onrender.com/api";

const instance = axios.create({
  baseURL: baseURL,
});

export const getLLMResponse = (data) => {
  return instance.post(
    // `http://localhost:5173/api/getLLMResponse`,
    // `http://localhost:8080/getLLMResponse`,
    // `${serverDomain}/getLLMResponse`,
    `getLLMResponse`,
    data
  );
};
