// const express = require("express");
// const bcrypt = require("bcrypt");
// const pool = require("../db");
// const router = express.Router();

// router.post("/login", async (req, res) => {
//   const { username, password } = req.body;
//   try {
//     const [rows] = await pool.query("SELECT * FROM users WHERE username = ?", [username]);
//     if (rows.length === 0) return res.status(401).json({ message: "User not found" });

//     const user = rows[0];
//     const match = await bcrypt.compare(password, user.password);
//     if (!match) return res.status(401).json({ message: "Invalid password" });

//     req.session.user = { id: user.user_id, username: user.username };
//     res.json({ message: "Login successful", userId: user.user_id });
//   } catch (err) {
//     console.error(err);
//     res.status(500).json({ message: "Server error" });
//   }
// });

// module.exports = router;


const express = require("express");
const router = express.Router();
const db = require("../db"); // file kết nối MySQL

router.post("/login", async (req, res) => {
  const { username, password } = req.body;
  try {
    const [rows] = await db.query("SELECT * FROM users WHERE username = ?", [username]);
    if (rows.length === 0) return res.status(401).json({ error: "Sai tài khoản hoặc mật khẩu" });

    const user = rows[0];
    const match = (password === user.password); // tạm thời chưa mã hóa
    // const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(401).json({ error: "Sai tài khoản hoặc mật khẩu" });
    req.session.user = { id: user.user_id, username: user.username };
    // login thành công → trả về userId
    res.json({ userId: user.student_id });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Lỗi server" });
  }
});

module.exports = router;
