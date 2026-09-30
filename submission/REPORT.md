# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Phạm Đức Anh
- **MSSV:** 2A202602994
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/phamducanh552004/K4-L3A-DAY13-PhamDucAnh-2A202602994-Monitoring-LLMOps
- **Commit SHA cuối:** Cập nhật sau khi commit và push phiên bản nộp.
- **Challenge ID:** Chờ Lab Coach release file riêng tại `config/challenge.json`.
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602994`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `evidence/01-pytest.png` |
| Log validator | `evidence/02-log-validator.png` |
| Dashboard validator | `evidence/03-dashboard-validator.png` |
| Structured log | `evidence/04-structured-log.png` |
| PII redaction | `evidence/05-pii-redaction.png` |
| Trace list | `evidence/06-trace-list.png` |
| Trace waterfall | `evidence/07-trace-waterfall.png` |
| Trace metadata | `evidence/08-trace-metadata.png` |
| Prompt versions | `evidence/09-prompt-versions.png` |
| Prompt rollback | `evidence/10-prompt-rollback.png` |
| Dashboard runtime | `evidence/11-dashboard-overview.png` |
| Incident metric | `evidence/12-incident-metric.png` |
| Incident log | `evidence/13-incident-log.png` |
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | Starter có TODO | 100/100; thiếu field/enrichment/PII leak đều bằng 0 | Chạy sau workload 12 request. |
| `validate_dashboard.py` | Contract starter | Hợp lệ 6/6 panel | Dashboard contract giữ time range 60 phút, refresh 30 giây. |
| `pytest` | Chưa lưu baseline | 23 passed | Có 1 cảnh báo deprecation từ dependency `anyio`, không có test fail. |
| Số traces hợp lệ | 0 | 12 root traces | 10 workload baseline, 1 v2 và 1 sau rollback v1. |
| Số PII leak | Chưa đo baseline | 0 | Validator quét email, điện thoại, CCCD và thẻ. |
| Latency P95 / TTFT P95 | Không dùng để kết luận | 1418 ms / 50 ms | Giá trị dashboard tại thời điểm chạy workload. |
| Retrieval success rate | Không dùng để kết luận | 100% | Lấy từ event `response_sent.tool_success`. |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Middleware xóa context cũ, dùng `x-request-id` nếu có hoặc sinh `req-<8-hex>`, bind vào structlog và trả lại bằng response header.
- **Các metadata được ghi vào structured log:** `user_id_hash`, `session_id`, `feature`, `model`, `env`, `correlation_id`, latency, TTFT, token, cost, quality và trạng thái retrieval.
- **Cách bảo đảm PII được scrub trước khi ghi:** `scrub_event` chạy trước JSON renderer/file writer, quét mọi chuỗi lồng nhau bằng rule email, điện thoại Việt Nam, CCCD, thẻ thanh toán và passport.
- **Cách kiểm chứng kết quả:** Workload có email/điện thoại/thẻ mẫu; `validate_logs.py` báo 0 PII leak và đạt 100/100.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Project `day13-k4-l3a-2A202602994` có 12 root trace do workload local tạo.
- **Cấu trúc root/retrieval/generation observations:** Root `lab-agent-run` chứa child `retrieval` và `generation`; generation có model, prompt đã scrub, usage và cost.
- **Cách nối trace với log:** Cùng `correlation_id` trong metadata Langfuse và structured log, ví dụ v2 `req-9d703d0f`, v1 rollback `req-0ff0758a`.
- **Prompt name:** `day13-chat`.
- **Version/label baseline:** v1, labels `baseline`, `production`.
- **Version/label candidate:** v2, label `candidate`; đã được promote `production` để tạo trace kiểm tra.
- **Trace ID của mỗi version:** v2 `2605544c172c7cf769202cfb4d6ba59f`; v1 sau rollback `005a62e3807bb9443a2d97ceee708d5b`.
- **Cách promote và rollback `production`:** Promote v2 bằng label `production`, chạy request v2, rồi chuyển `production` về v1 và chạy request xác minh.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Endpoint `/dashboard` đọc `data/logs.jsonl` và hiển thị latency/TTFT, traffic, errors/retrieval, cost, tokens và quality trong cửa sổ 60 phút.
- **SLO và lý do chọn:** `fast_successful_requests` đặt mục tiêu 99.5% request thành công trong 28 ngày, với latency ≤ 3000 ms; ngưỡng phù hợp contract và workload hiện tại.
- **Cách tính error budget:** Error budget là 0.5% tổng request trong cửa sổ 28 ngày.
- **Ba alert và runbook tương ứng:** `api_latency_p95_slo_breach`, `api_error_rate_high`, `retrieval_success_rate_low`; cấu hình ở `config/alert_rules.yaml` và hướng dẫn ở `docs/alerts.md`.

## 7. Điều tra challenge

- **Challenge ID:** Chưa có — Lab Coach chưa release `config/challenge.json`.
- **Khoảng thời gian điều tra:** Chưa chạy challenge chính thức.
- **Triệu chứng từ metrics:** Chưa kết luận khi không có challenge được cấp.
- **Log line và correlation ID liên quan:** Chờ challenge.
- **Trace ID và span gây ảnh hưởng:** Chờ challenge.
- **Root cause:** Chờ evidence Metrics → Logs → Traces của challenge.
- **Fix action:** Chờ xác định root cause.
- **Preventive measure:** Chờ xác định root cause.

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** Dùng FastAPI HTML dashboard thay vì thêm framework mới; sáu panel đọc trực tiếp structured log nên dễ chạy lại và đúng data source của contract.
- **Một lỗi/blocker đã gặp:** Chưa có prompt `day13-chat` nên app fallback về `local-v1`.
- **Cách tìm nguyên nhân và xử lý:** Log Langfuse trả 404 prompt; tạo v1/v2 trên project cá nhân, kiểm tra `production_version=1` và `candidate_version=2` sau rollback.
- **Cách hiểu luồng Metrics → Logs → Traces:** Metrics phát hiện triệu chứng; log lọc request theo correlation ID; trace cùng ID phân rã thời gian root/retrieval/generation để tìm bước gây ảnh hưởng.
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** Prompt label cho phép thử candidate rồi quay về baseline không cần redeploy; token/cost và SLO giúp cân bằng chất lượng với độ tin cậy và chi phí.
- **Điều quan trọng nhất đã học:** Validator chỉ kiểm tra contract; evidence runtime mới chứng minh hệ thống quan sát hoạt động với dữ liệu thật.
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** CP3 và evidence incident chờ file challenge riêng do Lab Coach cấp; không tự tạo hoặc thay thế file này.

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
