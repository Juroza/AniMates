import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import http from "http";
import SocketIO from "socket.io";
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

app.use(express.static(path.join(__dirname, "../frontend/dist")));

app.use((req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/dist/index.html"));
});
const port = process.env.PORT || 8080;
server.listen(port, () => {
  console.log("Server running on port", port);
});

const io = new SocketIO(server, {
  cors: {
    origin: FRONTEND_URL,
    methods: ["GET", "POST"],
  },
});

io.on("connection", (socket) => {});
