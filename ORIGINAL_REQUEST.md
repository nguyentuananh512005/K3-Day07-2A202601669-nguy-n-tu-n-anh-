# Original User Request

## Initial Request — 2026-08-03T10:02:35Z

Hệ thống tự động thu thập tài liệu quy chế/dịch vụ sinh viên của Đại học Bách khoa Hà Nội (HUST), định dạng Markdown để nạp vào cơ sở tri thức RAG, đồng thời xuất bản bản Word (.docx) chuẩn thể thức văn bản hành chính Việt Nam.

Working directory: `c:\Users\Admin\Desktop\lab\K3-Day07-2A202601669-nguy-n-tu-n-anh-`
Integrity mode: development

## Requirements

### R1. Thu thập dữ liệu quy chế học vụ HUST bằng Firecrawl
- Tìm kiếm và thu thập từ 5 đến 10 tài liệu, quy định, hướng dẫn dịch vụ chính thức của Đại học Bách khoa Hà Nội (từ các trang chính thống như `hust.edu.vn`, `ctt-daotao.hust.edu.vn`...).
- Các chủ đề cần bao phủ: Quy chế đào tạo (tín chỉ, đăng ký học phần), quy định học phí, chính sách học bổng (khuyến khích học tập, Trần Đại Nghĩa), quy định thư viện Tạ Quang Bửu, và nội quy ký túc xá.
- Mỗi tài liệu thu thập được phải lưu trữ dưới dạng file `.md` trong thư mục `data/` và chứa YAML front matter đầy đủ các trường: `id`, `title`, `source_url`, `retrieved_at`, `document_version`, `audience` (ví dụ: `student`, `faculty`, `staff`), `category`.

### R2. Xuất bản tài liệu Word (.docx) chuẩn thể thức hành chính Việt Nam
- Với mỗi tài liệu thu thập được, tự động chuyển đổi/tạo ra một file Word tương ứng (`.docx`) lưu tại thư mục `data/word/`.
- File Word phải được thiết kế và định dạng nghiêm túc theo chuẩn thể thức văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP):
  - Có Quốc hiệu: "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" (in hoa, đậm, canh giữa)
  - Có Tiêu ngữ: "Độc lập - Tự do - Hạnh phúc" (chữ thường, đậm, canh giữa, có gạch chân phía dưới)
  - Có tên cơ quan ban hành: "ĐẠI HỌC BÁCH KHOA HÀ NỘI" (in hoa, đứng)
  - Tiêu đề văn bản rõ ràng, số ký hiệu văn bản (nếu có).
  - Định dạng font chữ hành chính chuẩn (Times New Roman), canh lề chuẩn, định dạng heading và bảng biểu rõ ràng, sạch sẽ.
  - Sử dụng thư viện `python-docx` để tạo file Word tự động.

### R3. Nạp dữ liệu vào Vector Store & Chạy Benchmark
- Triển khai toàn bộ logic code còn lại trong `src/store.py` và `src/agent.py` để vượt qua 42 bài unit test (`pytest tests/ -v`).
- Sử dụng file `ingest.py` để nạp các tài liệu Markdown đã thu thập ở R1 vào `EmbeddingStore` với embedding thật (`EMBEDDING_PROVIDER=local`).
- Thiết lập **5 câu hỏi đánh giá (Benchmark Queries)** kèm câu trả lời chuẩn (Gold Answers) dựa trên tài liệu thực tế của HUST. Trong đó có ít nhất một câu hỏi yêu cầu lọc metadata `audience="student"`.
- Thực hiện chạy thử nghiệm truy xuất và ghi nhận kết quả đánh giá chi tiết vào `report/REPORT_NHOM.md` và `report/REPORT_CANHAN.md`.

## Acceptance Criteria

### Thể thức và Dữ liệu
- [ ] Có ít nhất 5 tài liệu thực tế của HUST được thu thập dưới dạng file `.md` trong thư mục `data/`.
- [ ] Mọi file `.md` đều có YAML front matter hợp lệ chứa đầy đủ thông tin truy vết.
- [ ] Có file `data/sources.csv` thống kê chi tiết các nguồn tài liệu đã lấy.
- [ ] Có thư mục `data/word/` chứa các file `.docx` tương ứng cho mỗi tài liệu.
- [ ] Các file `.docx` có đầy đủ Quốc hiệu, Tiêu ngữ, tên cơ quan ban hành ("ĐẠI HỌC BÁCH KHOA HÀ NỘI") canh lề và trình bày chuẩn Nghị định 30/2020/NĐ-CP.

### Kỹ thuật và Unit Test
- [ ] Lệnh `pytest tests/ -v` trả về kết quả thành công 100% (vượt qua tất cả 42 unit tests).
- [ ] Tích hợp và nạp thành công dữ liệu HUST thông qua `ingest.py` sử dụng `LocalEmbedder`.
- [ ] Có script chạy thử nghiệm truy xuất trên 5 câu hỏi benchmark hiển thị kết quả chính xác (có lọc metadata).

### Báo cáo
- [ ] File `report/REPORT_NHOM.md` và `report/REPORT_CANHAN.md` được viết đầy đủ nội dung theo cấu trúc yêu cầu của bài tập K3.
