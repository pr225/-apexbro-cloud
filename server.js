
const express = require("express");
const OpenAI = require("openai");
const helmet = require("helmet");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(helmet());
app.use(express.json({ limit: "30kb" }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/api/health", (req, res) => {
  res.json({ status: "ok", name: "ApexBro Personal AI" });
});

app.post("/api/chat", async (req, res) => {
  try {
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey) {
      return res.status(500).json({
        error: "OPENAI_API_KEY server environment mein set nahi hai."
      });
    }

    const { message, history = [] } = req.body;

    if (typeof message !== "string" || !message.trim()) {
      return res.status(400).json({ error: "Message bhejo." });
    }

    if (message.length > 10000 || !Array.isArray(history)) {
      return res.status(400).json({ error: "Input bahut bada hai." });
    }

    const client = new OpenAI({ apiKey });

    const safeHistory = history
      .filter(item =>
        item &&
        ["user", "assistant"].includes(item.role) &&
        typeof item.content === "string"
      )
      .slice(-10)
      .map(item => ({
        role: item.role,
        content: item.content.slice(0, 4000)
      }));

    const response = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content:
            "Tum ApexBro ho, ek helpful personal AI assistant. " +
            "User se Hindi, Hinglish ya uski pasand ki language mein baat karo. " +
            "Sahi, clear aur practical jawab do. Agar kisi action ki permission " +
            "ya external tool ki zaroorat ho, to uske baare mein saaf batao."
        },
        ...safeHistory,
        { role: "user", content: message.trim() }
      ]
    });

    res.json({
      reply: response.choices[0]?.message?.content || "Koi jawab nahi mila."
    });
  } catch (error) {
    console.error("AI request failed:", error.message);
    res.status(500).json({
      error: "AI request fail hui. API key, model access aur server logs check karo."
    });
  }
});

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`ApexBro server running on port ${PORT}`);
});
