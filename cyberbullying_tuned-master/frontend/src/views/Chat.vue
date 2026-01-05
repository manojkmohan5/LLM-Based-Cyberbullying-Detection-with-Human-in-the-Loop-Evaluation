<template>
  <div class="app">
    <!-- SIDEBAR -->
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-logo">🥑</div>
        <div class="brand-text">
          <div class="brand-name">{{ userStore.name }}</div>
          <div class="brand-sub">LLM</div>
        </div>
      </div>

      <div class="sidebar-section-title">Friends</div>

      <div class="sidebar-chats">
        <button
          v-for="chat in sidebarDummies"
          :key="chat.id"
          class="sidebar-chat"
        >
          {{ chat.title }}
        </button>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main">
      <header class="topbar">
        <button class="new-chat-btn" @click="closeChat">☓ Close Chat</button>
      </header>

      <!-- CHAT AREA -->
      <section class="chat-area" ref="chatWindowRef">
        <div
          v-for="message in messages"
          :key="message.id"
          class="message-row"
          :class="message.role"
        >
          <div class="message-bubble">
            <p
              v-for="(line, i) in message.text.split('\n')"
              :key="i"
              class="message-line"
            >
              {{ line }}
            </p>
          </div>
        </div>
      </section>

      <!-- INPUT -->
      <footer class="composer">
        <div class="composer-box">
          <textarea
            v-model="draft"
            class="composer-input"
            placeholder="Ask me anything . . ."
            rows="1"
            @keydown.enter.exact.prevent="sendMessage"
          ></textarea>

          <button
            class="composer-send-btn"
            type="button"
            :disabled="!draft.trim()"
            @click="sendMessage"
          >
            ➤
          </button>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useUserStore } from "../stores/user";
import { apiSwitch } from "../stores/apiSwitch";
import { v4 as uuid } from "uuid";

// Store (name, age, ethnicity)
const userStore = useUserStore();

// Dummy sidebar items
const sidebarDummies = [
  { id: 1, title: "Andrew" },
  { id: 2, title: "Benjamin" },
  { id: 3, title: "Cassey" },
  { id: 4, title: "Daniel" },
];

// Initial fake conversation
function getInitialMessages() {
  return [
    {
      id: uuid(),
      role: "assistant",
      text: "Hello, I just moved to the area.",
    },
    {
      id: uuid(),
      role: "assistant",
      text: "Would you like to be friends?",
    },
    {
      id: uuid(),
      role: "assistant",
      text: "I'm from Taiwan, btw 😊",
    },
    {
      id: uuid(),
      role: "user",
      text: "You are not welcomed! Go back home!",
    },
  ];
}

const messages = ref(getInitialMessages());
const draft = ref("");
const chatWindowRef = ref(null);

// [TODO]: testing
onMounted(() => {
  console.log("Name:", userStore.name);
  console.log("Age:", userStore.age);
  console.log("Ethnicity:", userStore.ethnicity);
  scrollToBottom();
});

watch(messages, scrollToBottom, { deep: true });

function scrollToBottom() {
  const el = chatWindowRef.value;
  if (!el) return;
  requestAnimationFrame(() => {
    el.scrollTop = el.scrollHeight;
  });
}

function resetChat() {
  messages.value = getInitialMessages();
}

function closeChat() {
  resetChat();
  window.open("https://forms.gle/MUsynVmuZU9bfesN8", "_blank");
}

async function sendMessage() {
  const text = draft.value.trim();
  if (!text) return;

  // Add user message
  messages.value.push({
    id: uuid(),
    role: "user",
    text,
  });

  draft.value = "";

  try {
    const request = {
      age: userStore.age,
      ethnicity: userStore.ethnicity,
      message: text,
    };
    const response = await apiSwitch("getLLMResponse", request);
    const data = response.data;

    // [TODE]: testing
    console.log("LLM Returned:", data);

    // Sample LLM api response format, single layered ->  {"flag": 1, "response": "LLM-generated reply"} or {"flag": -1, "response": null}
    // If flag == -1, the message is NOT identified as cyberbullying by system, do nothing
    if (data.flag == -1) {
      return;
    }
    // If flag == 1, the message is identified as cyberbullying by system
    if (data.flag == 1 && data.response) {
      messages.value.push({
        id: uuid(),
        role: "assistant",
        text: data.response,
      });
      
      // Add feedback prompt at the end if available
      if (data.feedback_prompt) {
        messages.value.push({
          id: uuid(),
          role: "assistant",
          text: data.feedback_prompt,
        });
      }
    }
  } catch (err) {
    // Show error message if API fails
    messages.value.push({
      id: uuid(),
      role: "assistant",
      text:
        "⚠️ Sorry, something went wrong connecting to the server.\n\n" +
        err.message,
    });
  }
}

// ========================================================================================================================
</script>

<style scoped>
/* Layout */
.app {
  display: flex;
  height: 100vh;
  height: auto;
  width: 100%;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: #111827;
  color: #e5e7eb;
  padding: 24px 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* FIX: ensures full height even when content scrolls */
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 32px;
}

.brand-logo {
  width: 40px;
  height: 40px;
  border-radius: 9999px;
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
  color: #f9fafb;
}

.brand-text {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 0.9rem;
}

.brand-name {
  font-weight: 600;
}

.brand-sub {
  color: #a5b4fc;
  font-weight: 700;
}

.sidebar-section-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #9ca3af;
  margin-bottom: 12px;
}

.sidebar-chats {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Chat buttons */
.sidebar-chat {
  border: none;
  background: transparent;
  color: #e5e7eb;
  text-align: left;
  padding: 8px 0;
  font-size: 0.9rem;
  cursor: pointer;
  opacity: 0.8;
}

.sidebar-chat:hover {
  opacity: 1;
}

/* Main area */
.main {
  flex: 1;
  background: #f4f3fb;
  display: flex;
  flex-direction: column;
  margin: 0 10%;
}

/* Top bar */
.topbar {
  display: flex;
  justify-content: flex-end;
  padding: 24px 5px;
}

/* New chat button */
.new-chat-btn {
  border: none;
  background: #000000;
  color: #f9fafb;
  padding: 1.5% 20px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(88, 28, 135, 0.3);
}

/* Chat area */
.chat-area {
  flex: 1;
  padding: 24px 80px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Messages */
.message-row {
  max-width: 640px;
}

.message-row.user {
  align-self: flex-end;
}

.message-row.assistant {
  align-self: flex-start;
}

/* user bubble */
.message-row.user .message-bubble {
  background: #a855f7;
  color: #f9fafb;
  padding: 1.5% 20px;
  border-radius: 20px;
  font-size: 0.9rem;
}

/* assistant card */
.message-row.assistant .message-bubble {
  background: #ffffff;
  color: #111827;
  padding: 1.5% 20px;
  border-radius: 20px;
  font-size: 0.9rem;
  line-height: 1.6;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.message-line + .message-line {
  margin-top: 4px;
}

/* Composer */
.composer {
  padding: 0 80px 32px;
}

.composer-box {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  background: #f9fafb;
  border-radius: 9999px;
  border: 1px solid #e5d9ff;
  display: flex;
  align-items: center;
  padding: 8px 14px;
  box-shadow: 0 16px 30px rgba(148, 163, 184, 0.25);
  gap: 8px;
}

.composer-input {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  outline: none;
  font-size: 0.95rem;
  color: #111827;
}

.composer-input::placeholder {
  color: #9ca3af;
}

.composer-send-btn {
  width: 32px;
  height: 32px;
  border-radius: 9999px;
  border: none;
  background: #a855f7;
  color: #fff;
  cursor: pointer;
}
</style>
