"""
run_benchmark.py — Script chạy nạp dữ liệu và đánh giá 5 Benchmark Queries cho HUST RAG (K3 Variant).
Sử dụng LocalEmbedder (SentenceTransformers) với EMBEDDING_PROVIDER=local.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(override=True)

# Cấu hình sử dụng LocalEmbedder
os.environ["EMBEDDING_PROVIDER"] = "local"

from ingest import build_knowledge_base
from src.agent import KnowledgeBaseAgent
from src.chunking import SentenceChunker
from src.embeddings import LocalEmbedder

DATA_DIR = Path("data")

BENCHMARK_QUERIES = [
    {
        "id": 1,
        "query": "Tiêu chuẩn và điều kiện xét cấp Học bổng Khuyến khích Học tập sinh viên HUST loại A (Xuất sắc) về GPA và DRL?",
        "filter": {"audience": "student"},
        "gold_answer": "Đạt Điểm trung bình học kỳ (GPA) ≥ 3.60 / 4.00 và Điểm rèn luyện (DRL) ≥ 90 điểm (loại Xuất sắc), không bị kỷ luật từ mức khiển trách trở lên trong học kỳ xét học bổng. Mức tiền học bổng bằng 150% mức học phí của tất cả các học phần sinh viên đăng ký.",
        "target_doc": "hoc-bong-khuyen-khich-hoc-tap"
    },
    {
        "id": 2,
        "query": "Khối lượng học tập tối thiểu và tối đa mà sinh viên HUST có học lực bình thường được phép đăng ký trong một học kỳ chính là bao nhiêu tín chỉ?",
        "filter": None,
        "gold_answer": "Sinh viên có học lực bình thường được phép đăng ký tối thiểu 12 tín chỉ và tối đa 24 tín chỉ trong một học kỳ chính.",
        "target_doc": "quy-che-dao-tao-tin-chi"
    },
    {
        "id": 3,
        "query": "Hạn nộp học phí tại Đại học Bách khoa Hà Nội được quy định như thế nào và hậu quả khi nộp quá hạn?",
        "filter": None,
        "gold_answer": "Sinh viên phải hoàn thành nộp học phí trước tuần thứ 4 của học kỳ. Nếu quá hạn sẽ bị hủy đăng ký học phần và không được tham gia thi kết thúc học phần.",
        "target_doc": "quy-dinh-hoc-phi"
    },
    {
        "id": 4,
        "query": "Theo Nội quy Sử dụng Thư viện Tạ Quang Bửu HUST, sinh viên được mượn tối đa bao nhiêu tài liệu về nhà và thời hạn mượn là bao nhiêu ngày?",
        "filter": None,
        "gold_answer": "Sinh viên được mượn tối đa 5 tài liệu/sách về nhà trong thời hạn 30 ngày, có thể gia hạn 1 lần (thêm 15 ngày).",
        "target_doc": "quy-dinh-thu-vien-ta-quang-buu"
    },
    {
        "id": 5,
        "query": "Quy định giờ giấc đóng mở cổng Ký túc xá HUST và các hành vi bị nghiêm cấm trong phòng ở KTX là gì?",
        "filter": None,
        "gold_answer": "Cổng KTX mở lúc 05:00 sáng và đóng lúc 23:00 tối hàng ngày. Nghiêm cấm đun nấu bằng bếp điện/bếp gas trong phòng, tàng trữ chất cháy nổ, uống rượu bia, đánh bạc và cho người ngoài ở lại qua đêm.",
        "target_doc": "noi-quy-ky-tuc-xa"
    }
]


def demo_llm(prompt: str) -> str:
    """Gọi LLM thật qua OpenAI API Cheap."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "deepseek-v4-flash"),
            messages=[
                {"role": "system", "content": "Bạn là trợ lý học tập hỗ trợ trả lời câu hỏi của sinh viên dựa trên văn bản quy định của Đại học Bách khoa Hà Nội (HUST). Hãy trả lời ngắn gọn, chính xác bằng tiếng Việt dựa theo ngữ cảnh được cung cấp."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Error calling LLM]: {e}", flush=True)
        lines = prompt.splitlines()
        context_part = "\n".join([line for line in lines if line.startswith("Context:") or (not line.startswith("Question:"))])
        return f"[RAG Agent Fallback] Extracted facts: {context_part[:250].strip()}..."


def run_benchmark():
    print("==========================================================", flush=True)
    print("MILESTONE 4: R3 INGESTION & BENCHMARK EVALUATION (K3)", flush=True)
    print("==========================================================", flush=True)

    # 1. Khởi tạo LocalEmbedder
    print("\n[1] Khởi tạo LocalEmbedder...", flush=True)
    embedder = LocalEmbedder()
    print(f"-> LocalEmbedder initialized with model: {embedder.model_name}", flush=True)

    # 2. Ingest dữ liệu từ data/
    print("\n[2] Nạp dữ liệu từ thư mục data/ vào EmbeddingStore...", flush=True)
    chunker = SentenceChunker(max_sentences_per_chunk=4)
    store = build_knowledge_base(DATA_DIR, embedding_fn=embedder, chunker=chunker, collection_name="hust_benchmark_kb")
    print(f"-> Ingestion hoàn tất. Đã nạp {store.get_collection_size()} chunks vào EmbeddingStore.", flush=True)

    # 3. Chạy 5 Benchmark Queries
    print("\n[3] Thực thi 5 Benchmark Queries...", flush=True)
    agent = KnowledgeBaseAgent(store=store, llm_fn=demo_llm)

    results = []
    total_score = 0

    for item in BENCHMARK_QUERIES:
        qid = item["id"]
        qtext = item["query"]
        filt = item["filter"]
        gold = item["gold_answer"]
        target = item["target_doc"]

        print(f"\n----------------------------------------------------------", flush=True)
        print(f"Query #{qid}: {qtext}", flush=True)
        if filt:
            print(f"Metadata Filter: {filt}", flush=True)

        if filt:
            top_chunks = store.search_with_filter(qtext, metadata_filter=filt, top_k=3)
        else:
            top_chunks = store.search(qtext, top_k=3)

        agent_response = agent.answer(qtext, top_k=3, metadata_filter=filt)

        print(f"Top 3 Chunk Results:", flush=True)
        found_target = False
        top1_target = False

        for rank, res in enumerate(top_chunks, start=1):
            doc_id = res["metadata"].get("doc_id", "N/A")
            score = res["score"]
            snippet = res["content"][:100].replace("\n", " ")
            print(f"  Rank {rank}: [score={score:.4f}] doc_id={doc_id} -> {snippet}...", flush=True)
            if target in doc_id or doc_id in target:
                found_target = True
                if rank == 1:
                    top1_target = True

        # Tính điểm retrieval score (2, 1, hoặc 0 theo docs/SCORING.md)
        if top1_target and found_target:
            score_pts = 2
        elif found_target:
            score_pts = 1
        else:
            score_pts = 0

        total_score += score_pts

        print(f"Agent Response preview: {agent_response[:150]}...", flush=True)
        print(f"Evaluated Score: {score_pts} / 2 pts", flush=True)

        results.append({
            "query_id": qid,
            "query": qtext,
            "filter": filt,
            "gold_answer": gold,
            "top_chunks": [
                {
                    "rank": i + 1,
                    "doc_id": c["metadata"].get("doc_id"),
                    "score": round(c["score"], 4),
                    "snippet": c["content"][:120]
                }
                for i, c in enumerate(top_chunks)
            ],
            "agent_response": agent_response,
            "score": score_pts
        })

    print("\n==========================================================", flush=True)
    print(f"BENCHMARK COMPLETED: Total Score = {total_score} / 10 pts", flush=True)
    print("==========================================================", flush=True)

    # Saved results file
    output_file = Path(".agents/worker_m4/benchmark_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Recorded detailed benchmark results to: {output_file.resolve()}", flush=True)
    return total_score


if __name__ == "__main__":
    run_benchmark()
