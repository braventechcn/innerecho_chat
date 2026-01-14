import React, { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import styled from "styled-components";
import { InputBar } from "./InputBar.jsx";
import { MessageBubble } from "./MessageBubble.jsx";
import { sendChatMessage } from "../services/api.js";

const Shell = styled.div`
  max-width: 880px;
  margin: 0 auto;
  padding: 24px;
  display: grid;
  gap: 16px;
`;

const Header = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Title = styled.h1`
  margin: 0;
  font-size: clamp(26px, 4vw, 32px);
  letter-spacing: -0.01em;
`;

const Subtitle = styled.p`
  margin: 0;
  color: var(--muted);
  line-height: 1.6;
`;

const ChatPanel = styled.div`
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 460px;
  max-height: 70vh;
  position: relative;
  z-index: 1; /* keep above background glows */
`;

const ScrollArea = styled.div`
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-right: 6px;
  position: relative;
  z-index: 1;
`;

function makeUserId() {
  return `guest-${Math.random().toString(36).slice(2, 8)}`;
}

export function ChatLayout() {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      role: "assistant",
      content: "你好，我是 InnerEcho。想聊聊最近的心情或遇到的困扰吗？",
    },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);

  const userId = useMemo(() => makeUserId(), []);

  const handleSend = async () => {
    if (!input.trim() || sending) return;
    const text = input.trim();
    setInput("");

    const pendingId = `user-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: pendingId, role: "user", content: text },
      { id: `${pendingId}-pending`, role: "assistant", content: "...", pending: true },
    ]);

    setSending(true);
    try {
      const data = await sendChatMessage({ userId, message: text });
      setMessages((prev) =>
        prev
          .filter((m) => !m.pending)
          .concat({
            id: `${pendingId}-reply`,
            role: "assistant",
            content: data.reply,
            latency: data.latency_ms,
          })
      );
    } catch (error) {
      setMessages((prev) =>
        prev.filter((m) => !m.pending).concat({
          id: `${pendingId}-error`,
          role: "assistant",
          content: "抱歉，后端暂时没有回应，请稍后再试。",
        })
      );
    } finally {
      setSending(false);
    }
  };

  return (
    <Shell>
      <Header>
        <Title>InnerEcho · 对话原型</Title>
        <Subtitle>输入一段文字，后端会调用大模型 API 并返回回复。</Subtitle>
      </Header>
      <ChatPanel>
        <ScrollArea>
          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div key={msg.id} layout>
                <MessageBubble role={msg.role} content={msg.content} latency={msg.latency} />
              </motion.div>
            ))}
          </AnimatePresence>
        </ScrollArea>
        <InputBar value={input} onChange={setInput} onSend={handleSend} disabled={sending} />
      </ChatPanel>
    </Shell>
  );
}
