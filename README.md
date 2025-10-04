
## 📝 Giới thiệu
**Mini App E-Learning là một ứng dụng hỗ trợ học tập trực tuyến dành cho sinh viên và giảng viên**  
Ứng dụng cung cấp các chức năng chính như: học theo môn học & chủ đề, làm quiz, thi thử và thi chính thức, quản lý tiến độ, tham gia thảo luận, và nhận phản hồi.  
Hệ thống được xây dựng dựa trên cơ sở dữ liệu  với các bảng quản lý user, môn học, bài tập, kỳ thi, tiến độ, chat, forum, và gamification (huy hiệu, bảng xếp hạng).  

## 👥 Thành viên nhóm  
- [Hoàng Cường](https://1yn3r.github.io/)  - Leader   
- [Nguyễn Thái Tuấn](https://lucksnow.github.io/)  
- [Phùng Anh Lực](https://lucdpt3105.github.io/) 
- [Hoàng Quang Minh](https://minh7709.github.io) 

## 📘 Mini App E-Learning

### 🚀 Chức năng chính
- 👩‍🎓 **Student**: Đăng nhập, tham gia môn học, xem tài liệu, làm quiz/thi, nộp bài tập, theo dõi tiến độ, nhận huy hiệu.  
- 👨‍🏫 **Teacher**: Tạo chủ đề, ra đề, quản lý câu hỏi, chấm điểm, phản hồi, tổ chức meeting online.  
- 👨‍💼 **Admin**: Quản lý user, môn học, gói subscription, báo cáo và thống kê.  
- ⚙️ **System**: Gửi thông báo, nhắc deadline, cập nhật leaderboard, backup dữ liệu.  

### 🗄️ Database
Cơ sở dữ liệu chính bao gồm:  
- `users`, `subjects`, `topics`, `studymaterials`  
- `questions`, `answers`, `exams`, `practicetests`, `results`  
- `progress`, `notes`, `sessions`  
- `badges`, `leaderboard`, `challenges`  
- `chatgroups`, `chatmessages`, `forumquestions`, `forumanswers`, `meetings`  
- `payments`, `subscriptions`, `announcements`, `feedbacks`  

### ⚡ Công nghệ sử dụng
- **Backend**: Python (Django) + MySQL  
- **Frontend**: HTML/CSS/JS (có thể nâng cấp React/Next.js)  
- **Database**: MySQL (script trong `DBMiniAppStudy.sql`)  
- **Testing**: Jest (unit test), Selenium (integration test)  
- **Quản lý mã nguồn**: Git/GitHub  
- **Mô hình phát triển**: Agile – Scrum  
