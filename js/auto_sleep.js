import { app } from "../../scripts/app.js";

const TITLES = {
  off: "Auto sleep after queue: off",
  armed: "Auto sleep after queue: on (click to turn off)",
  countdown: "Sleeping soon (click to cancel)",
};

const style = document.createElement("style");
style.textContent = `
#auto-sleep-button { gap: 5px; padding: 5px; border: 1px solid #555; border-radius: 5px; background: #2a2c2e; color: white; }
#auto-sleep-button:hover { background: var(--comfy-input-bg); }
#auto-sleep-button i { font-size: 18px; line-height: 18px; }
#auto-sleep-button[data-state="off"] i { opacity: 0.5; }
#auto-sleep-button[data-state="off"]:hover i { opacity: 1; }
#auto-sleep-button[data-state="armed"] { color: #4ade80; }
#auto-sleep-button[data-state="countdown"] { color: #f87171; }
`;
document.head.append(style);

const button = document.createElement("button");
button.id = "auto-sleep-button";
button.className = "comfyui-button";
const icon = document.createElement("i");
icon.className = "mdi mdi-power-sleep";
const label = document.createElement("span");
button.append(icon, label);

let timer = null;

function render({ state, remaining }) {
  clearInterval(timer);
  button.title = TITLES[state];
  button.dataset.state = state;
  label.textContent = "";
  label.style.display = state === "countdown" ? "" : "none";
  if (state === "countdown") {
    const end = Date.now() + remaining * 1000;
    const tick = () => {
      label.textContent = `${Math.max(0, Math.round((end - Date.now()) / 1000))}s`;
    };
    tick();
    timer = setInterval(tick, 1000);
  }
}

async function request(path, method) {
  const response = await app.api.fetchApi(path, { method });
  render(await response.json());
}

button.onclick = () => request("/auto_sleep/toggle", "POST");

app.registerExtension({
  name: "ComfyUI.AutoSleep",
  setup() {
    app.menu?.settingsGroup.element.before(button);
    app.api.addEventListener("auto_sleep.status", (event) => render(event.detail));
    app.api.addEventListener("reconnected", () => request("/auto_sleep/status", "GET"));
    request("/auto_sleep/status", "GET");
  },
});
