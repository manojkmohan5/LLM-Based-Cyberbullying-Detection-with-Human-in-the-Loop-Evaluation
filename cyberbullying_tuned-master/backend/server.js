import express from "express";
import cors from "cors";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

app.post("/api/getLLMResponse", (req, res) => {
  console.log("Request received at /api/getLLMResponse");
  console.log("Payload:", req.body);

  const { age, ethnicity, message } = req.body;

  const scriptPath = path.join(__dirname, "model/run.py");
  const modelDir = path.join(__dirname, "model");

  const py = spawn("python3", [scriptPath, message, age, ethnicity], {
    cwd: modelDir,
    env: process.env,
  });

  let output = "";
  let errorOutput = "";

  py.stdout.on("data", (data) => {
    output += data.toString();
  });

  py.stderr.on("data", (data) => {
    errorOutput += data.toString();
  });

  py.on("close", (code) => {
    console.log("Python exited with code:", code);
    console.log("Python STDOUT:", output);
    console.log("Python STDERR:", errorOutput);

    if (code !== 0) {
      return res.status(500).json({
        error: "Python script failed",
        detail: errorOutput,
      });
    }

    let parsed;
    try {
      parsed = JSON.parse(output.trim());
    } catch (e) {
      return res.status(500).json({
        error: "Invalid JSON from Python",
        raw: output,
      });
    }

    res.json(parsed);
  });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
