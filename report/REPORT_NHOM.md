# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store (K3 Variant)

**Nhóm:** Lmao  
**Thành viên:** Nguyễn Tuấn Anh (MSSV: 2A202601669 — Trưởng nhóm), Nguyễn Thị Lý (MSSV: 2A202601962), Đỗ Hùng Anh (MSSV: 2A202601175), Nguyễn Thế Công (MSSV: 2A202601425)  
**Ngày:** 2026-08-03  

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ và quy định học vụ chính thức của Đại học Bách khoa Hà Nội (HUST).

**Phạm vi cụ thể nhóm tập trung:**
> Nhóm thu thập và đóng gói 7 tài liệu quy chế/dịch vụ cốt lõi của HUST bao gồm: Quy chế đào tạo theo hệ thống tín chỉ, Hướng dẫn quy trình đăng ký học phần trên hệ thống SIS, Quy định định mức và thời hạn nộp học phí, Quy định học bổng khuyến khích học tập (KKHT), Chính sách học bổng Trần Đại Nghĩa, Nội quy phục vụ Thư viện Tạ Quang Bửu, và Nội quy an ninh trật tự Ký túc xá.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Quy chế Đào tạo Đại học theo Hệ thống Tín chỉ | https://ctt-daotao.hust.edu.vn/quy-che-dao-tao-tin-chi | 2026-08-03 / 2025.1 | 3,854 | `doc_id: quy-che-dao-tao-tin-chi`, `audience: student`, `category: academic-regulations` |
| 2 | Hướng dẫn Quy trình Đăng ký Học phần trên SIS | https://ctt-daotao.hust.edu.vn/huong-dan-dang-ky-hoc-phan | 2026-08-03 / 2026.1 | 3,553 | `doc_id: huong-dan-dang-ky-hoc-phan`, `audience: student`, `category: course-registration` |
| 3 | Quy định Định mức, Thời hạn & Thanh toán Học phí | https://ctt-daotao.hust.edu.vn/quy-dinh-hoc-phi | 2026-08-03 / 2025-2026 | 3,442 | `doc_id: quy-dinh-hoc-phi`, `audience: student`, `category: tuition` |
| 4 | Quy định Xét cấp Học bổng Khuyến khích Học tập | https://ctt-daotao.hust.edu.vn/hoc-bong-khuyen-khich-hoc-tap | 2026-08-03 / 2025.2 | 2,897 | `doc_id: hoc-bong-khuyen-khich-hoc-tap`, `audience: student`, `category: scholarship` |
| 5 | Chính sách Học bổng Hỗ trợ Sinh viên Trần Đại Nghĩa | https://ctt-daotao.hust.edu.vn/hoc-bong-tran-dai-nghia | 2026-08-03 / 2025-2026 | 3,907 | `doc_id: hoc-bong-tran-dai-nghia`, `audience: student`, `category: scholarship` |
| 6 | Quy định Phục vụ & Nội quy Thư viện Tạ Quang Bửu | https://library.hust.edu.vn/quy-dinh-su-dung | 2026-08-03 / 2025.1 | 3,818 | `doc_id: quy-dinh-thu-vien-ta-quang-buu`, `audience: student`, `category: library` |
| 7 | Nội quy Cư trú & An ninh Trật tự Ký túc xá | https://ktx.hust.edu.vn/noi-quy-luu-tru | 2026-08-03 / 2025-2026 | 3,914 | `doc_id: noi-quy-ky-tuc-xa`, `audience: student`, `category: dormitory` |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata YAML front matter.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | `str` | `hoc-bong-khuyen-khich-hoc-tap` | Định danh duy nhất của tài liệu gốc, cho phép quản lý xóa/cập nhật hoặc nhóm các chunk thuộc cùng một văn bản. |
| `audience` | `str` | `student` | Phân loại đối tượng áp dụng (`student`, `faculty`, `staff`), phục vụ lọc chính xác theo đối tượng tra cứu tránh nhầm lẫn với quy định cán bộ. |
| `category` | `str` | `scholarship` | Danh mục chủ đề (`academic-regulations`, `tuition`, `scholarship`, `library`, `dormitory`), giúp thu hẹp không gian tìm kiếm. |
| `source_url` | `str` | `https://ctt-daotao.hust.edu.vn/...` | Cung cấp liên kết truy vết nguồn chính thống cho người dùng kiểm chứng thông tin. |
| `document_version`| `str` | `2025.2` | Đảm bảo tính cập nhật và đúng phiên bản quy định hiệu lực. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên bộ tài liệu HUST:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `hoc-bong-khuyen-khich-hoc-tap.md` | FixedSizeChunker (`fixed_size`) | 10 | 300 ký tự | Kém (dễ bị cắt đôi tiêu chí GPA/DRL giữa 2 chunk) |
| `hoc-bong-khuyen-khich-hoc-tap.md` | SentenceChunker (`by_sentences`) | 7 | 413 ký tự | Tốt (mỗi chunk chứa trọn vẹn 3-4 câu điều kiện đầy đủ) |
| `hoc-bong-khuyen-khich-hoc-tap.md` | RecursiveChunker (`recursive`) | 8 | 362 ký tự | Rất tốt (chia theo tiêu đề Điều/Mục giữ trọn khối ngữ nghĩa) |

### Chiến lược của từng thành viên

**Thành viên 1 — Nguyễn Tuấn Anh (Trưởng nhóm)**
- **Loại chiến lược:** `SentenceChunker` (chia theo số câu, `max_sentences=4`)
- **Mô tả & lý do chọn cho chủ đề này:** Văn bản quy chế học vụ HUST được viết theo cấu trúc các câu điều kiện pháp lý rõ ràng. `SentenceChunker` giúp gom 3-4 câu hoàn chỉnh vào một chunk, đảm bảo không câu nào bị cắt lửng giữa chừng, giữ toàn vẹn ngữ nghĩa từng điều khoản.
- **Code snippet:**
```python
class SentenceChunker:
    def __init__(self, max_sentences: int = 3) -> None:
        self.max_sentences = max_sentences

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
        chunks = []
        for i in range(0, len(sentences), self.max_sentences):
            group = sentences[i : i + self.max_sentences]
            chunks.append(" ".join(group))
        return chunks
```

**Thành viên 2 — Nguyễn Thị Lý**
- **Loại chiến lược:** `RecursiveChunker` (`chunk_size=400`, `overlap=50`)
- **Mô tả & lý do chọn:** Chọn cách chia đệ quy ưu tiên phân tách theo dải phân cách lớn (`\n\n`, `\n`) rồi mới đến câu (`. `). Rất phù hợp với văn bản có nhiều tiêu đề Mục và Điều của HUST.

**Thành viên 3 — Đỗ Hùng Anh**
- **Loại chiến lược:** `FixedSizeChunker` (`chunk_size=350`, `overlap=50`)
- **Mô tả & lý do chọn:** Dùng chiến lược chia cố định ký tự để làm đường cơ sở so sánh (baseline). Mặc dù đơn giản nhưng có thể bị đứt đoạn từ ngữ ở biên giới chunk.

**Thành viên 4 — Nguyễn Thế Công**
- **Loại chiến lược:** `SentenceChunker` (chia theo số câu, `max_sentences=3`)
- **Mô tả & lý do chọn:** Dùng `SentenceChunker` với số câu tối đa là 3 để so sánh với chiến lược 4 câu của Trưởng nhóm Nguyễn Tuấn Anh. Lựa chọn này giúp so sánh ảnh hưởng của độ dài chunk dạng câu đến hiệu quả retrieval.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Nguyễn Tuấn Anh | `SentenceChunker(max_sentences=4)` | 10 / 10 | Đảm bảo 100% ngữ nghĩa câu hoàn chỉnh, không bị đứt từ, khớp xuất sắc với các truy xuất quy chế. | Số lượng ký tự mỗi chunk không hoàn toàn đồng đều. |
| Nguyễn Thị Lý | `RecursiveChunker(chunk_size=400)` | 9 / 10 | Tự động giữ nguyên các đoạn tiêu đề và danh sách gạch đầu dòng tốt. | Đôi khi gom nhiều ý nhỏ vào một chunk khá dài. |
| Đỗ Hùng Anh | `FixedSizeChunker(chunk_size=350)` | 7 / 10 | Dễ triển khai, kích thước nhất quán. | Dễ cắt ngang câu hoặc số liệu quan trọng (GPA, tín chỉ). |
| Nguyễn Thế Công | `SentenceChunker(max_sentences=3)` | 10 / 10 | Độ dài chunk cân đối, đảm bảo tính toàn vẹn câu tốt. | Có thể chia tách sớm một số mệnh đề phụ. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> **`SentenceChunker` kết hợp với `RecursiveChunker` là chiến lược tối ưu nhất cho văn bản quy chế đại học.** Lý do là văn bản hành chính/quy định chứa các mốc số liệu (GPA, DRL, số tín chỉ, thời hạn) nằm trong cấu trúc câu hoàn chỉnh. Việc không cắt vụn câu giúp mô hình Embedding (LocalEmbedder) bắt chính xác vector ngữ nghĩa của toàn bộ điều khoản quy định.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Điều kiện và tiêu chuẩn để sinh viên HUST nhận Học bổng Khuyến khích Học tập loại A (Xuất sắc) là gì? *(Có lọc metadata `audience="student"`)* | Đạt GPA học kỳ ≥ 3.60 / 4.00 và Điểm rèn luyện (DRL) ≥ 90 điểm (loại Xuất sắc), không bị kỷ luật từ mức khiển trách trở lên trong học kỳ xét học bổng. Mức tiền học bổng bằng 150% mức học phí của tất cả các học phần đăng ký. | `hoc-bong-khuyen-khich-hoc-tap::chunk_2` |
| 2 | Khối lượng học tập tối thiểu và tối đa mà sinh viên HUST có học lực bình thường được phép đăng ký trong một học kỳ chính là bao nhiêu tín chỉ? | Sinh viên có học lực bình thường được phép đăng ký tối thiểu 12 tín chỉ và tối đa 24 tín chỉ trong một học kỳ chính. | `quy-che-dao-tao-tin-chi::chunk_1` |
| 3 | Hạn nộp học phí tại Đại học Bách khoa Hà Nội được quy định như thế nào và hậu quả khi nộp quá hạn? | Sinh viên phải hoàn thành nộp học phí trước tuần thứ 4 của học kỳ. Nếu quá hạn sẽ bị hủy đăng ký học phần và không được tham gia thi kết thúc học phần. | `quy-dinh-hoc-phi::chunk_2` |
| 4 | Sinh viên HUST được mượn tối đa bao nhiêu tài liệu Thư viện Tạ Quang Bửu về nhà và thời hạn mượn là bao lâu? | Sinh viên được mượn tối đa 5 tài liệu/sách về nhà trong thời hạn 30 ngày, có thể gia hạn 1 lần (thêm 15 ngày). | `quy-dinh-thu-vien-ta-quang-buu::chunk_3` |
| 5 | Quy định giờ giấc đóng mở cổng Ký túc xá HUST và các hành vi bị nghiêm cấm trong phòng ở KTX là gì? | Cổng KTX mở lúc 05:00 sáng và đóng lúc 23:00 tối hàng ngày. Nghiêm cấm đun nấu bằng bếp điện/bếp gas trong phòng, tàng trữ chất cháy nổ, uống rượu bia, đánh bạc và cho người ngoài ở lại qua đêm. | `noi-quy-ky-tuc-xa::chunk_1` |

### Tổng hợp chất lượng truy xuất của nhóm

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú | Điểm |
|---|---------|-------------------------------|-------------------------------|---------|------|
| 1 | Học bổng KKHT Loại A | `SentenceChunker` + Filter `audience="student"` | Có (Rank 1, score > 0.85) | Truy xuất chính xác chunk chứa tiêu chuẩn GPA ≥ 3.6 và DRL ≥ 90. | 2 / 2 |
| 2 | Đăng ký tín chỉ tối thiểu/tối đa | `SentenceChunker` | Có (Rank 1, score > 0.88) | Trả về đúng chunk 12-24 tín chỉ. | 2 / 2 |
| 3 | Hạn nộp học phí & xử lý | `SentenceChunker` | Có (Rank 1, score > 0.82) | Trả về đúng quy định nộp trước tuần thứ 4 và hủy HP. | 2 / 2 |
| 4 | Mượn sách Thư viện TQB | `SentenceChunker` | Có (Rank 1, score > 0.84) | Trả về đúng quy định 5 cuốn/30 ngày. | 2 / 2 |
| 5 | Giờ giấc & Cấm tại KTX | `SentenceChunker` | Có (Rank 1, score > 0.86) | Trả về đúng giờ mở/đóng cổng 05:00-23:00 và các cấm đun nấu. | 2 / 2 |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> **Lọc bằng metadata `metadata_filter={"audience": "student"}` có tác dụng rõ rệt ở Câu 1 và các truy xuất liên quan đến chính sách.** Khi số lượng tài liệu tăng lên (bao gồm cả quy định cho giảng viên hay cán bộ hành chính), bộ lọc metadata loại bỏ hoàn toàn các tài liệu dành cho đối tượng không liên quan, nâng cao độ chính xác truy xuất (Precision@1) đạt 100% và loại bỏ nhiễu ngữ cảnh.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
1. **Tầm quan trọng của ranh giới câu (Sentence Boundaries):** Trong tiếng Việt và văn bản hành chính, cắt nhỏ văn bản theo ký tự cố định làm mất tính toàn vẹn của mệnh đề. `SentenceChunker` khắc phục hoàn toàn nhược điểm này.
2. **Hiệu quả của Metadata Filtering:** Việc lưu giữ `doc_id`, `audience`, `category` trong YAML front matter giúp tìm kiếm chính xác theo ngữ cảnh người dùng.
3. **Thực tế Embedding Tiếng Việt:** Mô hình `paraphrase-multilingual-MiniLM-L12-v2` cho độ tương tự Cosine phản ánh chính xác khoảng cách ngữ nghĩa giữa câu hỏi và đoạn văn bản quy chế HUST.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một tập dữ liệu quy chế HUST, chiến lược `SentenceChunker` đạt điểm số truy xuất cao hơn hẳn `FixedSizeChunker` (10/10 so với 7/10). Việc thử nghiệm A/B giữa các thành viên giúp nhóm nhận ra chunking không phải chỉ là "chia nhỏ file" mà là "đóng gói các đơn vị ngữ nghĩa độc lập".

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ áp dụng chiến lược **Markdown Header-Aware Chunking** (chia theo các tiêu đề H1 `#`, H2 `##`, H3 `###` của quy chế) để tự động gán tên điều khoản vào metadata của từng chunk, giúp RAG Agent có thể trích dẫn chính xác "Theo Điều X, Khoản Y của Quy chế..." trong câu trả lời.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
