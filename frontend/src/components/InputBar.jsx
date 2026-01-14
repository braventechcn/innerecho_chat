import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";

const Bar = styled.div`
  display: flex;
  align-items: flex-end;
  gap: 10px;
  padding: 12px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  position: relative;
  z-index: 2;
  pointer-events: auto;
`;

const Textarea = styled.textarea`
  flex: 1;
  min-height: 56px;
  max-height: 200px;
  resize: vertical;
  background: #0b1220;
  color: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 15px;
  line-height: 1.6;
  outline: none;
  pointer-events: auto;

  &::placeholder {
    color: var(--muted);
  }
`;

const SendButton = styled(motion.button)`
  border: none;
  border-radius: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: #0b1220;
  font-weight: 700;
  cursor: pointer;
  min-width: 96px;
  box-shadow: 0 12px 36px rgba(92, 168, 242, 0.35);
`;

export function InputBar({ value, onChange, onSend, disabled }) {
  return (
    <Bar>
      <Textarea
        placeholder="输入你的想法..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onSend();
          }
        }}
        autoFocus
        disabled={disabled}
      />
      <SendButton
        whileTap={{ scale: 0.97 }}
        whileHover={{ scale: 1.02 }}
        onClick={onSend}
        disabled={disabled}
      >
        {disabled ? "发送中..." : "发送"}
      </SendButton>
    </Bar>
  );
}
