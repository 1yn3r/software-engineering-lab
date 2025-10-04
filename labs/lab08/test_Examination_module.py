
import pytest
from unittest.mock import patch, MagicMock
import Examination_module as exam


# ------------------ TEST XEM DANH SÁCH ĐỀ THI ------------------

def test_xem_de_thi_khong_co():
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.return_value = []
        exams = exam.xem_de_thi()
        assert exams == []


def test_xem_de_thi_co():
    fake_exams = [
        {"exam_id": 1, "exam_title": "Đề Toán", "exam_subject_id": 1, "exam_duration": 30, "total_marks": 10},
        {"exam_id": 2, "exam_title": "Đề Lý", "exam_subject_id": 2, "exam_duration": 45, "total_marks": 15},
    ]
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.return_value = fake_exams
        exams = exam.xem_de_thi()
        assert len(exams) == 2
        assert exams[1]["exam_title"] == "Đề Lý"


def test_xem_de_thi_nhieu_de():
    fake_exams = [{"exam_id": i, "exam_title": f"Đề {i}", "exam_subject_id": 1, "exam_duration": 30, "total_marks": 10} for i in range(1, 6)]
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.return_value = fake_exams
        exams = exam.xem_de_thi()
        assert len(exams) == 5


def test_xem_de_thi_thieu_truong_KeyError():
    fake_exams = [{"exam_title": "Đề lỗi"}]  # thiếu exam_id
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.return_value = fake_exams
        with pytest.raises(KeyError):
            exam.xem_de_thi()


def test_xem_de_thi_db_error():
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = Exception("DB error")
        with pytest.raises(Exception):
            exam.xem_de_thi()


def test_xem_de_thi_cursor_none():
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.return_value = None
        exams = exam.xem_de_thi()
        assert exams == []  # thay vì is None


# ------------------ TEST LÀM BÀI THI ------------------

def test_lam_bai_thi_chua_tung_lam(monkeypatch):
    user = {"user_id": 1, "user_name": "Nguyen Van A"}

    inputs = ["1", "2", "3"]  # exam_id =1, chọn đáp án 2, chọn đáp án 3
    def fake_input(_):
        return inputs.pop(0) if inputs else "1"
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [   # exams
                {"exam_id": 1, "exam_title": "Đề Toán", "exam_subject_id": 1, "exam_duration": 30, "total_marks": 10}
            ],
            [   # examquestions
                {"question_id": 1, "question_text": "2+2=?"},
                {"question_id": 2, "question_text": "5*3=?"}
            ],
            [   # answers câu 1
                {"answer_id": 1, "answer_question_id": 1, "answer_text": "3", "is_correct": 0},
                {"answer_id": 2, "answer_question_id": 1, "answer_text": "4", "is_correct": 1}
            ],
            [   # answers câu 2
                {"answer_id": 3, "answer_question_id": 2, "answer_text": "15", "is_correct": 1},
                {"answer_id": 4, "answer_question_id": 2, "answer_text": "20", "is_correct": 0}
            ]
        ]
        # fetchone cho kiểm tra is_correct
        mock_cursor.fetchone.side_effect = [
            {"is_correct": 1},  # đáp án 2 đúng
            {"is_correct": 1}   # đáp án 3 đúng
        ]

        exam.lam_bai_thi(user)

        # ✅ assert chặt chẽ hơn
        mock_cursor.execute.assert_any_call("INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)", (1, 1, 2)
        )




def test_lam_bai_thi_da_lam_roi(monkeypatch):
    user = {"user_id": 1, "user_name": "Nguyen Van A"}
    monkeypatch.setattr("builtins.input", lambda _: "1")
    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Toán", "exam_subject_id": 1, "exam_duration": 30, "total_marks": 10}],
            []  # đã thi
        ]
        exam.lam_bai_thi(user)
        assert not any("INSERT INTO userexams" in str(c[0][0]) for c in mock_cursor.execute.call_args_list)


def test_lam_bai_thi_sai_het(monkeypatch):
    user = {"user_id": 2, "user_name": "Tran Van B"}
    inputs = ["1", "1", "4"]  # luôn chọn đáp án sai

    def fake_input(prompt):
        return inputs.pop(0) if inputs else "1"
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Lý", "exam_subject_id": 2, "exam_duration": 45, "total_marks": 15}],
            [{"question_id": 1, "question_text": "1+1=?"}, {"question_id": 2, "question_text": "2*2=?"}],
            [{"answer_id": 1, "answer_text": "3", "is_correct": 0}, {"answer_id": 2, "answer_text": "4", "is_correct": 1}],
            [{"answer_id": 3, "answer_text": "5", "is_correct": 0}, {"answer_id": 4, "answer_text": "6", "is_correct": 1}],
        ]
        mock_cursor.fetchone.side_effect = [{"is_correct": 0}, {"is_correct": 0}]
        exam.lam_bai_thi(user)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
            (2, 1, 0)
        )


def test_lam_bai_thi_dung_sai_hoa(monkeypatch):
    user = {"user_id": 3, "user_name": "Le Van C"}
    inputs = ["1", "2", "4"]  # câu 1 đúng, câu 2 sai

    def fake_input(prompt):
        return inputs.pop(0) if inputs else "1"
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Hóa", "exam_subject_id": 3, "exam_duration": 60, "total_marks": 20}],
            [{"question_id": 1, "question_text": "2+2=?"}, {"question_id": 2, "question_text": "10/2=?"}],
            [{"answer_id": 1, "answer_text": "4", "is_correct": 1}, {"answer_id": 2, "answer_text": "5", "is_correct": 0}],
            [{"answer_id": 3, "answer_text": "4", "is_correct": 0}, {"answer_id": 4, "answer_text": "5", "is_correct": 1}],
        ]
        mock_cursor.fetchone.side_effect = [{"is_correct": 1}, {"is_correct": 0}]
        exam.lam_bai_thi(user)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
            (3, 1, 1)
        )


def test_lam_bai_thi_nhap_sai(monkeypatch):
    user = {"user_id": 4, "user_name": "Pham Van D"}
    inputs = ["1", "abc", "99", "2"]  # nhập sai nhiều lần, cuối cùng mới nhập hợp lệ

    def fake_input(prompt):
        return inputs.pop(0) if inputs else "2"
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Sinh", "exam_subject_id": 4, "exam_duration": 30, "total_marks": 10}],
            [{"question_id": 1, "question_text": "3*3=?"}],
            [{"answer_id": 1, "answer_text": "9", "is_correct": 1}, {"answer_id": 2, "answer_text": "6", "is_correct": 0}],
        ]
        mock_cursor.fetchone.return_value = {"is_correct": 1}
        exam.lam_bai_thi(user)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
            (4, 1, 1)
        )


def test_lam_bai_thi_bo_qua(monkeypatch):
    user = {"user_id": 5, "user_name": "Pham Van E"}
    inputs = ["1", ""]  # bỏ qua không nhập đáp án

    def fake_input(prompt):
        return inputs.pop(0) if inputs else ""
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Anh", "exam_subject_id": 5, "exam_duration": 60, "total_marks": 20}],
            [{"question_id": 1, "question_text": "What is 2+2?"}],
            [{"answer_id": 1, "answer_text": "4", "is_correct": 1}],
        ]
        mock_cursor.fetchone.return_value = None  # không đúng
        exam.lam_bai_thi(user)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
            (5, 1, 0)
        )


def test_lam_bai_thi_khong_co_dap_an(monkeypatch):
    user = {"user_id": 6, "user_name": "Pham Van F"}
    inputs = ["1", "1"]

    def fake_input(prompt):
        return inputs.pop(0) if inputs else "1"
    monkeypatch.setattr("builtins.input", fake_input)

    with patch.object(exam, "cursor", MagicMock()) as mock_cursor:
        mock_cursor.fetchall.side_effect = [
            [{"exam_id": 1, "exam_title": "Đề Tin", "exam_subject_id": 6, "exam_duration": 45, "total_marks": 15}],
            [{"question_id": 1, "question_text": "2*5=?"}],
            []  # không có đáp án nào
        ]
        mock_cursor.fetchone.return_value = None
        exam.lam_bai_thi(user)
        mock_cursor.execute.assert_any_call(
            "INSERT INTO userexams (user_exam_user_id, user_exam_exam_id, user_exam_score) VALUES (%s,%s,%s)",
            (6, 1, 0)
        )
