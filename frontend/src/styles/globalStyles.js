import { createGlobalStyle } from "styled-components";

export const GlobalStyles = createGlobalStyle`
  :root {
    --bg: #0f172a;
    --panel: #111827;
    --text: #e5e7eb;
    --muted: #9ca3af;
    --accent: #5ca8f2;
    --accent-2: #6ed3c2;
    --border: #1f2937;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    background: radial-gradient(circle at 20% 20%, rgba(92, 168, 242, 0.16), transparent 25%),
                radial-gradient(circle at 80% 0%, rgba(110, 211, 194, 0.12), transparent 26%),
                var(--bg);
    color: var(--text);
    min-height: 100vh;
  }

  #root {
    min-height: 100vh;
  }

  ::selection {
    background: rgba(92, 168, 242, 0.25);
  }
`;
