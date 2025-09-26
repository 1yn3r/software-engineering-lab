const express = require("express");
const pool = require("../db");
const router = express.Router();

// Lấy danh sách lecture của sinh viên
router.get("/my", async (req, res) => {
  const userId = req.session.user?.id;
  
  if (!userId) return res.status(401).json({ message: "Not logged in" });

  const [rows] = await pool.query(`
    SELECT l.* FROM student_lectures sl
    JOIN lectures l ON sl.lecture_id = l.lecture_id
    WHERE sl.user_id = ?
  `, [userId]);  
  res.json(rows);
});

router.get("/me", async (req, res) => {
    const userId = req.session.user?.id;
  
    if (!userId) return res.status(401).json({ message: "Not logged in when load user" });
  const [rows] = await pool.query(
    "SELECT username, fullname FROM users WHERE user_id = ?",
    [userId]
  );

  if (rows.length === 0) {
    return res.status(404).json({ error: "Không tìm thấy user" });
  }

  res.json(rows[0]);
});



// Tìm lecture theo code
router.post("/add", async (req, res) => {
  const userId = req.session.user?.id;
  const { code } = req.body;
  if (!userId) return res.status(401).json({ message: "Not logged in" });

  const [lectures] = await pool.query("SELECT * FROM lectures WHERE code = ?", [code]);
  if (lectures.length === 0) return res.status(404).json({ message: "Lecture not found" });

  const lecture = lectures[0];

  await pool.query("INSERT IGNORE INTO student_lectures (user_id, lecture_id) VALUES (?, ?)", [userId, lecture.lecture_id]);
  res.json({ message: "Lecture added", lecture });
});

// Lấy câu hỏi của 1 lecture
router.get("/:id/questions", async (req, res) => {
  const lectureId = req.params.id;
  const [questions] = await pool.query("SELECT * FROM questions WHERE lecture_id = ?", [lectureId]);
  res.json(questions);
});

module.exports = router;
