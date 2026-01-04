// =========================== server.js (native WebSockets) ===========================
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import http from "http";
import cors from "cors";
import axios from "axios";
import { WebSocketServer } from "ws";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);

const FRONTEND_URL = process.env.FRONTEND_URL || "http://localhost:5173";
app.use(cors({ origin: FRONTEND_URL }));
app.use(express.json());

const BACKEND_ENDPOINT =
  process.env.BACKEND_ENDPOINT || "http://localhost:7071";

// -------------------- REST PROXY ROUTES (unchanged) --------------------
app.post("/register", async (req, res) => {
  try {
    console.log("Received login request in Express proxy");
    const { username, password } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/register`,
      { username, password },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /player/login:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/login", async (req, res) => {
  try {
    console.log("Received login request in Express proxy");
    const { username, password } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/login`,
      { username, password },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /login:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/get-users-project", async (req, res) => {
  try {
    console.log("Received login request in Express proxy");
    const { username } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/get-users-project`,
      { name: username },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /login:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/create-new-project", async (req, res) => {
  try {
    console.log("Received create project request in Express proxy");
    const {
      name,
      owner,
      isPrivate,
      users,
      width,
      height,
      fps,
      datetime_created,
      datetime_modified,
      frameCount,
    } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/create-new-project`,
      {
        name,
        owner,
        private: isPrivate,
        users,
        width,
        height,
        fps,
        datetime_created,
        datetime_modified,
        frameCount,
      },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /login:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/edit-project", async (req, res) => {
  try {
    console.log("Received edit project request in Express proxy");
    const {
      name,
      owner,
      isPrivate,
      users,
      width,
      height,
      fps,
      datetime_created,
      datetime_modified,
      frameCount,
      id,
    } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/edit-project`,
      {
        project: {
          name,
          owner,
          private: isPrivate,
          users,
          width,
          height,
          fps,
          datetime_created,
          datetime_modified,
          frameCount,
        },
        id: id,
      },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /login:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/delete-project", async (req, res) => {
  try {
    console.log("Received delete-project request in Express proxy");
    const { name } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/delete-project`,
      { name },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /delete-project:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.get("/load-frame", async (req, res) => {
  try {
    console.log("Received load-frame request in Express proxy");
    const { name } = req.query;

    const apiRes = await axios.get(`${BACKEND_ENDPOINT}/load-frame`, {
      params: { name },
      headers: { "Content-Type": "application/json" },
    });

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /load-frame:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/get-all-users", async (req, res) => {
  try {
    console.log("Receivedget-all-users request in Express proxy");

    const apiRes = await axios.post(`${BACKEND_ENDPOINT}/get-all-users`, {
      headers: { "Content-Type": "application/json" },
    });

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /get-all-users:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/add-frame-to-project", async (req, res) => {
  try {
    console.log("Received add-frame-to-project request in Express proxy");
    const { projectName, strokeRecord, frameNumber } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/add-frame-to-project`,
      { projectName, strokeRecord, frameNumber },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /add-frame-to-project:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.get("/get-frame-url", async (req, res) => {
  try {
    console.log("Received get-frame-url request in Express proxy");
    const { name } = req.query;

    const apiRes = await axios.get(`${BACKEND_ENDPOINT}/get-frame-url`, {
      params: { name },
      headers: { "Content-Type": "application/json" },
    });

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /get-frame-url:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.post("/upload-frame", async (req, res) => {
  try {
    console.log("Received upload-frame request in Express proxy");
    const { fileName } = req.body;

    const apiRes = await axios.post(
      `${BACKEND_ENDPOINT}/upload-frame`,
      { fileName },
      { headers: { "Content-Type": "application/json" } }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /get-all-users:");
    if (error.response)
      res.status(error.response.status).json(error.response.data);
    else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

// -------------------- STATIC FRONTEND --------------------
app.use(express.static(path.join(__dirname, "../frontend/dist")));
app.use((req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/dist/index.html"));
});

const port = process.env.PORT || 8080;
server.listen(port, () => {
  console.log("Server running on port", port);
});

// ===================== WebSocket server (ws) =====================
const wss = new WebSocketServer({
  server,
  // you can optionally set a path:
  // path: "/ws",
});

// --- helpers ---
function safeSend(ws, obj) {
  if (ws.readyState !== ws.OPEN) return;
  try {
    ws.send(JSON.stringify(obj));
  } catch (e) {
    // ignore
  }
}

function roomFor(frameName) {
  return `frame:${frameName}`;
}

function wsInRoom(ws, frameName) {
  return ws.data?.frameName === frameName;
}

// roomName -> Set<ws>
const rooms = new Map();
function joinRoom(ws, roomName) {
  leaveRoom(ws);

  ws.data.roomName = roomName;

  if (!rooms.has(roomName)) rooms.set(roomName, new Set());
  rooms.get(roomName).add(ws);
}
function leaveRoom(ws) {
  const roomName = ws.data?.roomName;
  if (!roomName) return;
  const set = rooms.get(roomName);
  if (set) {
    set.delete(ws);
    if (set.size === 0) rooms.delete(roomName);
  }
  ws.data.roomName = null;
}

function broadcastRoom(roomName, messageObj, exceptWs = null) {
  const set = rooms.get(roomName);
  if (!set) return;
  for (const client of set) {
    if (exceptWs && client === exceptWs) continue;
    safeSend(client, messageObj);
  }
}

// ===================== in-memory frame sessions (same logic) =====================
const frameSessions = new Map();

async function loadFrameSession(frameName) {
  if (frameSessions.has(frameName)) return frameSessions.get(frameName);

  const apiRes = await axios.get(`${BACKEND_ENDPOINT}/load-frame`, {
    params: { name: frameName },
    headers: { "Content-Type": "application/json" },
  });

  const data = apiRes.data;
  const session = {
    frameName,
    projectName: data.projectName,
    frameNumber: data.frameNumber,
    strokeRecords: data.strokeRecord ?? [], // backend might return [] or string; client normalizes
    dirty: false,
    lastUpdate: Date.now(),
  };

  frameSessions.set(frameName, session);
  return session;
}

setInterval(async () => {
  const dirtySessions = [...frameSessions.values()].filter((s) => s.dirty);

  for (const s of dirtySessions) {
    try {
      await axios.post(
        `${BACKEND_ENDPOINT}/update-frame-data`,
        {
          name: s.frameName,
          strokeRecord: s.strokeRecords,
          frameNumber: s.frameNumber,
        },
        { headers: { "Content-Type": "application/json" } }
      );
      s.dirty = false;
    } catch (err) {
      console.error(
        "Failed to flush frame",
        s.frameName,
        err?.response?.data || err.message
      );
    }
  }
}, 2000);

// ===================== WebSocket protocol (event-based) =====================
// Incoming message format:
// { event: "joinFrame", data: { ... } }
//
// Outgoing messages follow same pattern.

wss.on("connection", (ws, req) => {
  ws.data = { frameName: null, roomName: null };

  console.log("ws connected");

  ws.on("message", async (raw, isBinary) => {
    try {
      // allow both text JSON and binary frames:
      // (we're using JSON everywhere; binary is used only if you decide to send raw PNG later)
      if (isBinary) {
        // If you ever decide to send PNG binary directly, handle it here.
        // For now we ignore unexpected binary messages.
        return;
      }

      const msg = JSON.parse(raw.toString("utf8"));
      const { event, data } = msg || {};
      if (!event) return;

      // -------- joinFrame --------
      if (event === "joinFrame") {
        const { frameName } = data || {};
        if (!frameName) return;

        // leave previous
        if (ws.data.frameName) {
          leaveRoom(ws);
        }

        ws.data.frameName = frameName;
        const roomName = roomFor(frameName);
        joinRoom(ws, roomName);

        console.log("joined", frameName);

        const session = await loadFrameSession(frameName);

        // to this socket only
        safeSend(ws, {
          event: "frameDataRetrieval",
          data: {
            frameName,
            strokeRecord: session.strokeRecords,
            frameNumber: session.frameNumber,
            projectName: session.projectName,
          },
        });

        // presence to others
        broadcastRoom(
          roomName,
          { event: "presence:joined", data: { socketId: "ws" } },
          ws
        );
        return;
      }

      // -------- frame:png --------
      if (event === "frame:png") {
        const { frameName, png } = data || {};
        if (!frameName || !wsInRoom(ws, frameName)) return;

        try {
          // client sends ArrayBuffer; when JSON-stringified it won't survive.
          // so we expect base64 here for native WS.
          // In the client rewrite below we send base64.
          const buffer = Buffer.from(png, "base64");

          const apiRes = await axios.post(
            `${BACKEND_ENDPOINT}/upload-frame`,
            buffer,
            {
              params: { filename: frameName },
              headers: { "Content-Type": "image/png" },
              maxBodyLength: Infinity,
            }
          );

          console.log("Uploaded PNG:", apiRes.status);
        } catch (err) {
          console.error("PNG upload failed:", err?.message || err);
        }
        return;
      }

      // -------- drawing:action --------
      if (event === "drawing:action") {
        const payload = data;
        const { frameName, type } = payload || {};
        if (!frameName) return;
        if (!wsInRoom(ws, frameName)) return;

        const session = await loadFrameSession(frameName);

        if (type === "stroke" && payload.stroke) {
          session.strokeRecords.push(payload.stroke);
        } else if (type === "clear") {
          session.strokeRecords = [];
        }

        session.dirty = true;
        session.lastUpdate = Date.now();

        const roomName = roomFor(frameName);
        broadcastRoom(roomName, {
          event: "drawing:action-confirmed",
          data: payload,
        });

        return;
      }

      // -------- drawing:get-actions --------
      if (event === "drawing:get-actions") {
        const { frameName } = data || {};
        if (!frameName) return;
        if (!wsInRoom(ws, frameName)) return;

        const session = await loadFrameSession(frameName);
        safeSend(ws, {
          event: "drawing:actions-snapshot",
          data: {
            frameName,
            strokeRecord: session.strokeRecords,
            frameNumber: session.frameNumber,
          },
        });
        return;
      }

      // ignore unknown events
    } catch (e) {
      console.error("ws message parse/handler error:", e?.message || e);
    }
  });

  ws.on("close", () => {
    const frameName = ws.data?.frameName;
    const roomName = ws.data?.roomName;
    leaveRoom(ws);

    if (frameName && roomName) {
      broadcastRoom(roomName, {
        event: "presence:left",
        data: { socketId: "ws" },
      });
    }
  });

  ws.on("error", (err) => {
    console.error("ws error", err?.message || err);
  });
});
