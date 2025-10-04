import mysql.connector
import getpass

# ------------------ KẾT NỐI MYSQL ------------------
conn = mysql.connector.connect(
        host="localhost",
        user="root",                   # user trong MySQL
        password="12345",              # mật khẩu của user
        database="learning2",          # tên database
        auth_plugin="mysql_native_password",
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        use_unicode=True
)
cursor = conn.cursor(dictionary=True)

# ------------------ HÀM ĐĂNG NHẬP ------------------
def login():
    print("===== ĐĂNG NHẬP SINH VIÊN =====")
    email = input("Email: ")
    pw = getpass.getpass("Mật khẩu: ")
    cursor.execute("SELECT * FROM users WHERE user_email=%s AND user_password=%s AND user_role='student'", (email, pw))
    user = cursor.fetchone()
    if user:
        print(f"✅ Xin chào {user['user_name']}!")
        return user
    else:
        print("❌ Sai thông tin đăng nhập!")
        return None

# ------------------ XEM DANH SÁCH ĐỀ THI ------------------
def xem_de_thi():
    cursor.execute("SELECT * FROM exams")
    exams = cursor.fetchall()
    if not exams:   # xử lý None hoặc rỗng
        print("❌ Hiện tại chưa có đề thi nào.")
        return []
    print("\n📋 DANH SÁCH ĐỀ THI:")
    for e in exams:
        print(f"{e['exam_id']}. {e['exam_title']} (Môn {e['exam_subject_id']}, Thời gian {e['exam_duration']} phút, Tổng điểm {e['total_marks']})")
    return exams

# ------------------ LÀM BÀI THI ------------------
def lam_bai_thi(user):
    exams = xem_de_thi()
    exam_id = int(input("👉 Nhập ID đề thi muốn làm: "))
    
    # Lấy câu hỏi trong đề
    cursor.execute("""
        SELECT q.question_id, q.question_text
        FROM examquestions eq
        JOIN questions q ON eq.exam_question_question_id = q.question_id
        WHERE eq.exam_question_exam_id = %s
    """, (exam_id,))
    questions = cursor.fetchall()
    if not questions:
        print("❌ Bạn đã làm bài thi này rồi, không thể làm lại.")
        return

    
    score = 0
    total = len(questions)
    
    print(f"\n===== BẮT ĐẦU LÀM ĐỀ THI {exam_id} =====")
    for q in questions:
        print(f"\nCâu {q['question_id']}: {q['question_text']}")
        cursor.execute("SELECT * FROM answers WHERE answer_question_id=%s", (q['question_id'],))
        answers = cursor.fetchall()
        for ans in answers:
            print(f"   {ans['answer_id']}. {ans['answer_text']}")
        max_retry = 3
        attempts = 0
        while attempts < max_retry:
            try:
                choice = int(input("👉 Chọn đáp án: "))
                if any(ans["answer_id"] == choice for ans in answers):
                    break
                else:
                    print("❌ Đáp án không tồn tại, vui lòng nhập lại.")
            except ValueError:
                print("❌ Lựa chọn không hợp lệ, vui lòng nhập số.")
            attempts += 1
        else:
            print("⚠️ Bạn đã nhập sai quá nhiều lần, bỏ qua câu hỏi này.")
            continue



        cursor.execute("SELECT is_correct FROM answers WHERE answer_id=%s", (choice,))
        result = cursor.fetchone()
        if result and result["is_correct"]:
            score += 1

    
    # Lưu điểm vào userexams
    cursor.execute("INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
                   (user['user_id'], exam_id, score))
    conn.commit()
    
    print(f"\n🎉 Hoàn thành! Bạn đúng {score}/{total} câu.")

# ------------------ MENU ------------------
def menu():
    user = login()
    if not user:
        return
    
    while True:
        print("\n===== MENU SINH VIÊN =====")
        print("1. Xem danh sách đề thi")
        print("2. Làm bài thi")
        print("0. Thoát")
        choice = input("➡️ Chọn thao tác: ")
        
        if choice == "1":
            xem_de_thi()
        elif choice == "2":
            lam_bai_thi(user)
        elif choice == "0":
            print("👋 Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

# ------------------ CHẠY CHƯƠNG TRÌNH ------------------
if __name__ == "__main__":
    menu()
    cursor.close()
    conn.close()
