import express from "express";
import OpenAI from "openai";
import cors from "cors";
import dotenv from "dotenv";
dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post("/api/getLLMResponse", async (req, res) => {
  try {
    const { message } = req.body;

    const completion = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content:
            "You classify a message as bullying or not. If NOT harmful, respond exactly with '-1'. If harmful, respond with a short message telling the user why the message is harmful.",
        },
        { role: "user", content: message },
      ],
    });

    const reply = completion.choices[0].message.content.trim();

    // --- Interpret the model reply ---
    if (reply === "-1") {
      return res.json({ flag: -1, response: null });
    }

    return res.json({ flag: 1, response: reply });
  } catch (err) {
    console.error(err);
    return res.status(500).json({
      flag: -1,
      error: err.message,
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
