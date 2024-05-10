import { Fragment, useEffect, useState } from "react";
import "./ChatPage.css";

interface Persona {
  name: string;
  description?: string;
  system_prompt?: string;
  tools: string[];
}

interface FormValue {
  input: string;
  temperature: string;
  persona: Persona;
}

function ChatPage({ version }: { version: string }) {
  const showToolsV1 = false
  const [personas, setPersonas] = useState<Persona[]>([]);

  const [formValue, setFormValue] = useState<FormValue>({
    input: "",
    temperature: "0.5",
    persona: {
      name: "",
      description: "",
      tools: []
    }
  });

  // Store id so when we clear the chat, we don't use the same memory
  const initialChatId = () => {
    const storedChatId = localStorage.getItem('chatId');
    return storedChatId ? storedChatId : crypto.randomUUID();
  }
  const [chatId, setChatId] = useState<string>(initialChatId);
  // Store messages in local storage, so we can persist them across endpoints & reloads
  const initialMessages = () => {
    const storedMessages = localStorage.getItem('messages');
    return storedMessages ? JSON.parse(storedMessages) : [];
  }
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>(initialMessages);

  const handleClearMessages = () => {
    setMessages([]);
    setChatId(crypto.randomUUID())
    localStorage.removeItem('messages')
    localStorage.removeItem('chatId');
  };

  async function getPersonas() {
    const response = await fetch("/api/v2/personas", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setPersonas([]);
    setFormValue({ input: formValue.input, temperature: formValue.temperature, persona: data.personas[0] })
    setPersonas(data.personas);
  }
  const getAllTools = (personas: Persona[]): String[] => {
    const allTools = personas.flatMap((persona: Persona) => persona.tools);
    const uniqueTools = Array.from(new Set(allTools));
    return uniqueTools.sort();
  }

  useEffect(() => {
    // Store messages in local storage
    localStorage.setItem('messages', JSON.stringify(messages));

    // Scroll to the bottom of the chat window
    const chatWindow = document.querySelector('.chat-window');
    if (chatWindow) {
      chatWindow.scrollTo(0, chatWindow.scrollHeight);
    }
  }, [messages]);

  useEffect(() => {
    if (version !== "v0") {
      getPersonas();
    }
  }, []);

  const handleMessageSend = async () => {
    if (formValue.input.trim()) {
      const requestToSend = formValue.input;
      setFormValue({ input: "", temperature: formValue.temperature, persona: formValue.persona })

      const newMessages = [...messages, { text: requestToSend, sender: "user" }];
      setMessages(newMessages);

      const requestBody = { chatId: chatId, question: requestToSend, temperature: formValue.temperature, persona: formValue.persona.name };
      console.log("Request Body: ", requestBody);
      const response = await fetch(`/api/${version.toLowerCase()}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages([...newMessages, { text: data.response, sender: "ai" }]);
      } else {
        setFormValue({ input: requestToSend, temperature: formValue.temperature, persona: formValue.persona });
        console.error("Failed to send message");
      }
    }
  };

  return (
    <div className="row">
      <div className="col-3">
        {version !== "v0" && (
          <div className="card">
            <div className="card-header">
              <span>Options</span>
            </div>
            <div className="card-body">
              {version === "v1" && showToolsV1 && (
                <section>
                  <div style={{ textAlign: "left" }}>
                    <span className="label">Tools Available:</span>
                    <br />
                    {getAllTools(personas).map((toolName: String, index: number) => (
                      <Fragment key={index}>
                        <div className="tag">{toolName}</div>
                      </Fragment>
                    )
                    )}
                  </div>
                </section>
              )}
              {version === "v2" && (
                <>
                  <div className="label">Personas</div>
                  <select
                    onChange={(e) => {
                      const selectedPersona = personas.find(persona => persona.name === e.target.value)
                      if (selectedPersona) {
                        setFormValue({
                          input: formValue.input,
                          temperature: formValue.temperature,
                          persona: selectedPersona
                        })
                      }
                    }}
                  >
                    {personas.map((persona) => {
                      return (
                        <option value={persona.name}>{persona.name}</option>
                      )
                    })}
                  </select>
                  <br />
                  <span id="persona-description">{formValue.persona.description}</span>
                  <br />
                  <br />
                  <div style={{ textAlign: "left" }}>
                    <span className="label">Tools Available:</span>
                    <br />
                    {formValue.persona.tools.map((tool: string, index) => (
                      <><div key={index} className="tag" >{tool}</div></>
                    ))}
                  </div>
                </>
              )}
              <br />
              <span className="label">Temperature</span>
              <br />
              <input
                type="range"
                onChange={(e) => setFormValue({
                  input: formValue.input,
                  persona: formValue.persona,
                  temperature: e.target.value
                })}
                value={formValue.temperature}
                min={0}
                max={1.0}
                step={0.05}
              ></input>
            </div>
          </div>
        )}
      </div>
      <div className={version !== "v0" ? "col-9" : "col-12"}>
        <div className="card">
          <div className="card-header">
            <span>Chat</span>
            <button
              onClick={handleClearMessages}
              id="clearButton"
            >
              Clear Chat
            </button>
          </div>
          <div className="card-body">
            <div className="chat-window">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.sender}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            <hr />
            <div className="row">
              <div className="col-12">
                <textarea
                  value={formValue.input}
                  rows={4}
                  onChange={(e) => setFormValue({
                    input: e.target.value,
                    persona: formValue.persona,
                    temperature: formValue.temperature
                  })}
                  onKeyDown={e => e.key === "Enter" && handleMessageSend()}
                />
              </div>
            </div>
            <div className="row" style={{ textAlign: "right" }}>
              <div className="col-12">
                <button
                  onClick={handleMessageSend}
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;
