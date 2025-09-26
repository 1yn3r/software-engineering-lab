const express = require("express");
const session = require("express-session");
const bodyParser = require("body-parser");
const authRoutes = require("./routes/auth");
const lectureRoutes = require("./routes/lectures");
const bcrypt = require("bcryptjs");


const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


app.use(session({
  secret: "supersecret",
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // nếu dùng https
}));

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/lectures", lectureRoutes);
app.use(express.static("public"));


app.listen(3000, () => console.log("Server running on http://localhost:3000"));
