# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store (K3 Variant)

**Họ tên:** Nguyễn Tuấn Anh  
**MSSV:** 2A202601669  
**Nhóm:** Lmao  
**Ngày:** 2026-08-03  

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao (gần 1.0) thể hiện hai vector biểu diễn văn bản chỉ cùng một hướng trong không gian vector nhiều chiều, nghĩa là hai câu hoặc đoạn văn bản đó chứa nội dung ngữ nghĩa rất tương đồng hoặc diễn đạt cùng một ý tưởng, bất kể độ dài ngắn khác nhau.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Sinh viên HUST phải hoàn thành nộp học phí trước tuần thứ 4 của học kỳ."
- Câu B: "Hạn chót thanh toán tiền học phí đối với sinh viên Bách khoa là tuần 4."
- Tại sao tương đồng: Cả hai câu cùng đề cập đến đối tượng sinh viên HUST/Bách khoa và mốc thời gian hạn nộp học phí là tuần thứ 4.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Sinh viên HUST phải hoàn thành nộp học phí trước tuần thứ 4 của học kỳ."
- Câu B: "Thư viện Tạ Quang Bửu cho phép sinh viên mượn tối đa 5 cuốn sách về nhà."
- Tại sao khác: Câu A nói về nghĩa vụ tài chính/học phí, còn Câu B nói về quy định mượn sách thư viện — hai chủ đề hoàn toàn độc lập.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Text embeddings thường có số chiều lớn và các vector được chuẩn hóa độ dài (L2 norm = 1.0). Khi đó, khoảng cách Euclid bị ảnh hưởng bởi độ dài văn bản (biến số biên độ), trong khi Cosine similarity chỉ đo góc giữa các vector — phản ánh đúng sự tương đồng về chủ đề ngữ nghĩa mà không bị nhiễu bởi số lượng từ hay độ dài đoạn văn.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, `chunk_size=500`, `overlap=50`. Bao nhiêu chunks?**
> **Trình bày phép tính:**
> Bước dịch chuyển (stride) giữa các chunk: $\text{step} = \text{chunk\_size} - \text{overlap} = 500 - 50 = 450$ ký tự.  
> Công thức tính số lượng chunk:
> $$\text{Number of Chunks} = \left\lceil \frac{N - \text{overlap}}{\text{chunk\_size} - \text{overlap}} \right\rceil = \left\lceil \frac{10000 - 50}{500 - 50} \right\rceil = \left\lceil \frac{9950}{450} \right\rceil = \lceil 22.11 \rceil = 23 \text{ chunks}$$
> **Đáp án:** 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Khi `overlap` tăng lên 100, bước dịch chuyển $\text{step} = 500 - 100 = 400$ ký tự.  
> Số lượng chunk mới: $\lceil (10000 - 100) / 400 \rceil = \lceil 9900 / 400 \rceil = \lceil 24.75 \rceil = 25$ chunks.  
> Ta muốn độ chồng chéo nhiều hơn để bảo toàn ngữ cảnh liên tục giữa các đoạn văn bản liền kề, tránh việc một thông tin hoặc ý nghĩa câu bị ngắt đôi đúng tại ranh giới phân chia chunk.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận khi lập trình các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng biểu thức chính quy (regex) `(?<=[.!?])\s+` để tách đoạn văn thành các câu dựa trên dấu kết thúc câu (`.`, `!`, `?`). Sau đó gom nhóm tối đa `max_sentences` câu liên tiếp vào một chunk. Xử lý các trường hợp ngoại lệ như chuỗi rỗng, khoảng trắng thừa, hoặc các đoạn văn không có dấu chấm bằng cách trả về danh sách sạch sẽ.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Áp dụng thuật toán đệ quy chia nhỏ với danh sách dải phân cách giảm dần `["\n\n", "\n", ". ", " "]`. Tại mỗi bước, nếu đoạn văn vượt quá `chunk_size`, hàm sẽ tách theo phân cách ưu tiên cao nhất hiện tại. Base case (trường hợp cơ sở) xảy ra khi độ dài đoạn văn nhỏ hơn hoặc bằng `chunk_size` hoặc đã duyệt hết các dải phân cách (khi đó buộc phải cắt cứng theo độ dài).

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lớp `EmbeddingStore` duy trì một danh sách các đối tượng `Document` cùng với một danh sách các vector nhúng (embeddings) được tính toán thông qua `embedding_fn`. Trong phương thức `search()`, tính điểm độ tương tự Cosine giữa vector của `query` với tất cả các vector nhúng lưu trong store bằng `compute_similarity()`, sau đó sắp xếp kết quả theo điểm số giảm dần và trả về top-k đoạn văn kèm thông tin `score`, `content`, `metadata`.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter()` lọc các ứng viên thỏa mãn điều kiện `metadata_filter` (ví dụ `audience == "student"`) trước khi xếp hạng độ tương tự Cosine, đảm bảo kết quả trả về khớp 100% điều kiện lọc. `delete_document(doc_id)` tìm và xóa tất cả các chunk có `metadata["doc_id"] == doc_id`, trả về `True` nếu có ít nhất 1 chunk bị xóa và `False` nếu không tìm thấy.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Phương thức `answer()` gọi `store.search()` (hoặc `search_with_filter()`) để trích xuất top-k chunk liên quan nhất. Sau đó xây dựng ngữ cảnh (context injection) theo cấu trúc prompt:  
> `Context:\n[Chunk 1]\n[Chunk 2]...\n\nQuestion: [query]\nAnswer using only the provided context.`  
> Cuối cùng truyền prompt này cho mô hình LLM (`llm_fn`) để sinh ra câu trả lời chính xác, minh bạch và truy vết được.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua toàn bộ 46 bài unit test trong dự án (`pytest tests/ -v`).

### Kết Quả Kiểm Thử (Test Results)

```text
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Admin\Desktop\lab\K3-Day07-2A202601669-nguy-n-tu-n-anh-
plugins: anyio-4.12.1, langsmith-0.10.10, asyncio-1.4.0
collected 46 items

tests/test_docx_converter.py::test_parse_front_matter PASSED             [  2%]
tests/test_docx_converter.py::test_docx_conversion_geometry_and_margins PASSED [  4%]
tests/test_docx_converter.py::test_administrative_header_content PASSED  [  6%]
tests/test_docx_converter.py::test_convert_all_harvested_documents PASSED [  8%]
tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [ 10%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [ 13%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [ 15%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [ 17%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 26%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 28%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 30%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 32%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 34%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 36%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 39%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 41%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 43%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 45%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 47%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 56%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 58%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 60%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 63%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 65%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 67%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 69%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 78%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 82%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 84%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 86%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 89%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 91%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 93%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================= 46 passed in 1.07s ==============================
```

**Số lượng bài test vượt qua (pass):** 46 / 46 (100% Pass)

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên được mượn tối đa 5 cuốn sách thư viện. | Thời hạn mượn tài liệu Thư viện Tạ Quang Bửu là 30 ngày. | cao | 0.785 | Đúng |
| 2 | Hạn nộp học phí là trước tuần thứ 4 của học kỳ. | Sinh viên nộp học phí chậm sẽ bị hủy đăng ký học phần. | cao | 0.812 | Đúng |
| 3 | Cổng Ký túc xá HUST đóng cửa lúc 23h hàng ngày. | Sinh viên được đăng ký ở KTX trực tuyến trên website. | cao | 0.741 | Đúng |
| 4 | Điểm trung bình GPA học kỳ đạt từ 3.60 trở lên. | Tiêu chuẩn nhận học bổng KKHT loại A xuất sắc. | cao | 0.864 | Đúng |
| 5 | Quy chế đào tạo đại học theo hệ thống tín chỉ HUST. | Hướng dẫn mượn tài liệu giáo trình Thư viện TQB. | thấp | 0.312 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp số 1 có điểm số tương tự thực tế khá cao (0.785) dù hai câu đề cập đến hai thông số khác nhau (số lượng sách vs số ngày mượn). Điều này cho thấy mô hình nhúng `paraphrase-multilingual-MiniLM-L12-v2` học được ngữ cảnh chung về "dịch vụ thư viện" rất tốt, nhóm các thuộc tính liên quan đến cùng chủ đề vào vùng không gian vector gần nhau.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân trong gói `src` với `SentenceChunker`.

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Điều kiện nhận Học bổng KKHT loại A? *(Lọc `audience="student"`)* | `hoc-bong-khuyen-khich-hoc-tap::chunk_2` (GPA ≥ 3.60, DRL ≥ 90, 150% học phí) | 0.864 | Có (Relevant) | Trích dẫn chính xác tiêu chuẩn GPA ≥ 3.60 và DRL ≥ 90 cho loại A. |
| 2 | Khối lượng đăng ký tín chỉ tối thiểu/tối đa? | `quy-che-dao-tao-tin-chi::chunk_1` (Bình thường: 12-24 tín chỉ, cảnh cáo Mức 1: tối đa 14 tín chỉ) | 0.881 | Có (Relevant) | Trả lời chính xác từ 12 đến 24 tín chỉ cho học lực bình thường. |
| 3 | Hạn nộp học phí và hậu quả quá hạn? | `quy-dinh-hoc-phi::chunk_2` (Hoàn thành trước tuần 4, quá hạn hủy đăng ký HP) | 0.825 | Có (Relevant) | Trả lời nộp trước tuần 4, quá hạn hủy đăng ký học phần. |
| 4 | Số lượng sách mượn và thời hạn mượn TQB? | `quy-dinh-thu-vien-ta-quang-buu::chunk_3` (Tối đa 5 tài liệu/30 ngày, gia hạn 1 lần) | 0.843 | Có (Relevant) | Trả lời tối đa 5 tài liệu trong 30 ngày. |
| 5 | Giờ đóng mở cổng & hành vi cấm tại KTX? | `noi-quy-ky-tuc-xa::chunk_1` (Mở 05:00, đóng 23:00, cấm đun nấu/rượu bia/đánh bạc) | 0.867 | Có (Relevant) | Trả lời mở 05:00, đóng 23:00 và liệt kê các hành vi bị cấm. |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5 (100% Relevance Rate)

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Qua quá trình làm bài và thảo luận nhóm, tôi học được rằng việc kết hợp metadata filtering với semantic retrieval giúp giải quyết triệt để bài toán nhầm lẫn ngữ cảnh đối tượng. Ngoài ra, việc lựa chọn chiến lược chunking phù hợp với định dạng văn bản (Sentence Chunking cho quy chế hành chính) đóng vai trò quyết định đến 80% chất lượng của hệ thống RAG.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
