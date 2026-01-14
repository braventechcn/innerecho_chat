import React from "react";
import styled from "styled-components";
import { ChatLayout } from "./components/ChatLayout.jsx";

const Background = styled.div`
  min-height: 100vh;
  padding: 32px 18px 42px;
  position: relative;
  overflow: hidden;
`;

const Glow = styled.div`
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 18% 18%, rgba(92, 168, 242, 0.28), transparent 32%),
    radial-gradient(circle at 82% 8%, rgba(110, 211, 194, 0.2), transparent 28%),
    radial-gradient(circle at 72% 72%, rgba(92, 168, 242, 0.14), transparent 32%);
  filter: blur(36px);
  opacity: 0.8;
`;

const Content = styled.div`
  position: relative;
  z-index: 1;
`;

function App() {
  return (
    <Background>
      <Glow />
      <Content>
        <ChatLayout />
      </Content>
    </Background>
  );
}

export default App;
