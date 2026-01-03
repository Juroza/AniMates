import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import http from "http";
import { Server } from "socket.io";
import cors from "cors";
import axios from "axios";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
const server = http.createServer(app);
const FRONTEND_URL = process.env.FRONTEND_URL || "http://localhost:5173";
app.use(cors({ origin: FRONTEND_URL }));
app.use(express.json());

const BACKEND_ENDPOINT =
  process.env.BACKEND_ENDPOINT || "http://localhost:7071";
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
      {
        projectName,
        strokeRecord,
        frameNumber,
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /add-frame-to-project:");
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
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
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    res.status(apiRes.status).json(apiRes.data);
  } catch (error) {
    console.error("Error calling backend /get-all-users:");
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      console.error(error.message);
      res
        .status(500)
        .json({ result: false, msg: "Backend service unreachable" });
    }
  }
});

app.use(express.static(path.join(__dirname, "../frontend/dist")));

app.use((req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/dist/index.html"));
});
const port = process.env.PORT || 8080;
server.listen(port, () => {
  console.log("Server running on port", port);
});

const io = new Server(server, {
  cors: {
    origin: FRONTEND_URL,
    methods: ["GET", "POST"],
  },
});

class FrameSessionState {
  constructor(frameName, strokeRecords, projectName) {
    this.frameName = frameName;
    this.strokeRecords = strokeRecords;
    this.projectName = projectName;
  }
}
function socketInRoom(socket, frameName) {
  return socket.rooms.has(roomFor(frameName));
}

const frameSessions = new Map();
function roomFor(frameName) {
  return `frame:${frameName}`;
}
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
    strokeRecords: data.strokeRecord ?? [], // whatever backend returns
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

io.on("connection", (socket) => {
  console.log("socket connected", socket.id);

  socket.data.frameName = null;

  socket.on("joinFrame", async ({ frameName }) => {
    if (socket.data.frameName) socket.leave(roomFor(socket.data.frameName));

    socket.data.frameName = frameName;
    socket.join(roomFor(frameName));
    console.log("joined", frameName);

    const session = await loadFrameSession(frameName);

    socket.emit("frameDataRetrieval", {
      frameName,
      strokeRecord: session.strokeRecords,
      frameNumber: session.frameNumber,
      projectName: session.projectName,
    });

    socket
      .to(roomFor(frameName))
      .emit("presence:joined", { socketId: socket.id });
  });
  socket.on("frame:png", async ({ frameName, png }) => {
    try {
      const buffer = Buffer.from(png);

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
      console.error("PNG upload failed:", err.message);
    }
  });

  socket.on("drawing:action", async (payload) => {
    const { frameName, type } = payload || {};
    if (!frameName) return;
    if (!socketInRoom(socket, frameName)) return;
    console.log("got draw", frameName);

    const session = await loadFrameSession(frameName);

    if (type === "stroke" && payload.stroke) {
      session.strokeRecords.push(payload.stroke);
    } else if (type === "clear") {
      session.strokeRecords = [];
    }

    session.dirty = true;
    session.lastUpdate = Date.now();

    io.to(roomFor(frameName)).emit("drawing:action-confirmed", payload);
  });

  socket.on("drawing:get-actions", async ({ frameName }) => {
    console.log("get actions", frameName);

    const session = await loadFrameSession(frameName);
    socket.emit("drawing:actions-snapshot", {
      frameName,
      strokeRecord: session.strokeRecords,
      frameNumber: session.frameNumber,
    });
  });

  socket.on("disconnect", () => {
    const frameName = socket.data.frameName;
    if (frameName) {
      socket
        .to(roomFor(frameName))
        .emit("presence:left", { socketId: socket.id });
    }
  });
});
