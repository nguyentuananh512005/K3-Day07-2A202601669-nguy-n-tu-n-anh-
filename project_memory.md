# Bộ não dự án — HUST Regulation RAG (Group: Lmao)

Dự án này triển khai hệ thống RAG (Retrieval-Augmented Generation) cục bộ để tra cứu và dịch các quy chế, dịch vụ sinh viên của Đại học Bách khoa Hà Nội (HUST), đồng thời hỗ trợ chuyển đổi tài liệu sang chuẩn văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP).

---

## 👥 Thông tin Nhóm

*   **Tên nhóm:** Lmao
*   **Thành viên:**
    *   Nguyễn Tuấn Anh (MSSV: 2A202601669 — Trưởng nhóm)
    *   Nguyễn Thị Lý (MSSV: 2A202601962)
    *   Đỗ Hùng Anh (MSSV: 2A202601175)
    *   Nguyễn Thế Công (MSSV: 2A202601425)

---

## 🛠️ Stack công nghệ & Cấu hình chính

*   **Ngôn ngữ lập trình:** Python 3.10+
*   **Mô hình Embedding:** `paraphrase-multilingual-MiniLM-L12-v2` (sử dụng `sentence-transformers` chạy offline hoàn toàn qua `LocalEmbedder`).
*   **Cơ sở dữ liệu Vector (Vector Store):** Triển khai lớp `EmbeddingStore` hỗ trợ in-memory fallback và ChromaDB.
*   **Trình tách văn bản (Chunking Strategy):**
    *   `SentenceChunker`: Tách văn bản theo regex kết thúc câu tiếng Việt, gom tối đa 4 câu/chunk. Đây là chiến lược tối ưu nhất cho văn bản quy chế.
    *   `RecursiveChunker`: Phân tách đệ quy dùng separators `["\n\n", "\n", ". ", " "]`.
*   **Xuất bản tài liệu Word:** Thư viện `python-docx` định dạng tài liệu đầu ra tuân thủ nghiêm ngặt chuẩn Nghị định 30/2020/NĐ-CP.

---

## 📂 Kiến trúc dữ liệu và Thư mục

*   `data/` — Tập tài liệu tri thức (Markdown) cào được từ các trang thông tin chính thống HUST.
*   `data/sources.csv` — File ghi nhận nguồn gốc và metadata truy vết tài liệu.
*   `data/word/` — Chứa 13 file Word hành chính tương ứng.
*   `report/` — Báo cáo nhóm (`REPORT_NHOM.md`) và báo cáo cá nhân (`REPORT_CANHAN.md`).
*   `src/` — Gói logic cốt lõi (`chunking.py`, `store.py`, `agent.py`).
*   `tests/` — Bộ kiểm thử tự động (46 bài test bao phủ).

---

## 📈 Kết quả Benchmark

Hệ thống RAG vượt qua 100% (5/5 câu hỏi benchmark) đạt độ tương tự Cosine tối ưu (0.82 - 0.88), có hỗ trợ Metadata Filtering (`audience="student"`) để tránh nhầm lẫn đối tượng quy chế.

---

## 🔒 Quy tắc Git Push (Bắt buộc)
*   Mọi hoạt động đẩy code lên Git (Commit & Push) **PHẢI** sử dụng tài khoản email: `nguyentuananh512005@gmail.com` (Name: `nguyentuananh512005`).
*   Tài khoản phải được cấu hình phạm vi local (`git config --local user.email ...`) trước khi push.
