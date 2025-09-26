const mysql = require("mysql2/promise");

const pool = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "12345",
  database: "e_learning"
});

module.exports = pool;
