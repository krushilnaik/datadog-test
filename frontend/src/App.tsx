import React, { useState } from "react";
import datadogRum from "./datadog";

export default function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const send = async () => {
    datadogRum.addAction("send_message", { message });

    const res = await fetch("http://backend:8000/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const text = await res.text();
    setResponse(text);

    datadogRum.addAction("received_response", { response: text });
  };

  return (
    <div style={{ padding: 20 }}>
      <input value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type a message" />
      <button onClick={send}>Send</button>
      <pre>{response}</pre>
    </div>
  );
}
