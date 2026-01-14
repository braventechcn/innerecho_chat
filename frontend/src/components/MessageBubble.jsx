import React from "react";
import { motion } from "framer-motion";
import styled from "styled-components";

const Bubble = styled(motion.div)`
  align-self: ${(props) => (props.role === "assistant" ? "flex-start" : "flex-end")};
  max-width: 88%;
  padding: 12px 14px;
  border-radius: 14px;
  background: ${(props) => (props.role === "assistant" ? "#1f2937" : "#2563eb")};
  color: ${(props) => (props.role === "assistant" ? "#e5e7eb" : "#f8fafc")};
  border: 1px solid var(--border);
  box-shadow: 0 12px 38px rgba(0, 0, 0, 0.18);
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 15px;
`;

const Meta = styled.div`
  font-size: 12px;
  color: var(--muted);
  margin-top: 6px;
  align-self: ${(props) => (props.role === "assistant" ? "flex-start" : "flex-end")};
`;

export function MessageBubble({ role, content, latency }) {
  return (
    <>
      <Bubble
        role={role}
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.18 }}
      >
        {content}
      </Bubble>
      {latency && (
        <Meta role={role}>响应耗时: {latency} ms</Meta>
      )}
    </>
  );
}
