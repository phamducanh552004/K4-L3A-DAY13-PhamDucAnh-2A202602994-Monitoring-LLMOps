# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1

- Tên: `api_latency_p95_slo_breach`
- Severity: warning
- Duration: 10m
- Kênh thông báo: Slack
- SLI/SLO liên quan: `fast_successful_requests`, latency P95 ≤ 3000 ms.
- Điều kiện và thời gian duy trì: latency P95 của `response_sent` > 3000 ms trong 10 phút.
- Ảnh hưởng tới người dùng: phản hồi chậm, có thể hết thời gian chờ.
- Ba bước kiểm tra đầu tiên: kiểm tra panel latency; lọc log theo correlation ID chậm; mở trace cùng ID để so sánh retrieval và generation.
- Mitigation tạm thời: tắt incident đang bật hoặc giảm tải workload; chỉ kết luận sau khi đối chiếu trace.
- Owner: Pham Duc Anh

## Alert 2

- Tên: `api_error_rate_high`
- Severity: critical
- Duration: 5m
- Kênh thông báo: Slack
- SLI/SLO liên quan: error rate ≤ 2%.
- Điều kiện và thời gian duy trì: `request_failed / request_received * 100 > 2` trong 5 phút.
- Ảnh hưởng tới người dùng: yêu cầu thất bại hoặc không nhận được câu trả lời.
- Ba bước kiểm tra đầu tiên: xem breakdown `error_type`; tìm log lỗi gần nhất; mở trace cùng correlation ID.
- Mitigation tạm thời: tắt `tool_fail` nếu đang bật và xác nhận request mới thành công.
- Owner: Pham Duc Anh

## Alert 3

- Tên: `retrieval_success_rate_low`
- Severity: warning
- Duration: 10m
- Kênh thông báo: Slack
- SLI/SLO liên quan: retrieval success rate ≥ 90%.
- Điều kiện và thời gian duy trì: tỷ lệ `tool_success` của retrieval < 90% trong 10 phút.
- Ảnh hưởng tới người dùng: câu trả lời thiếu ngữ cảnh hoặc lỗi truy xuất.
- Ba bước kiểm tra đầu tiên: kiểm tra error panel; lọc `tool_name=retrieval`; xem retrieval observation trong trace.
- Mitigation tạm thời: tắt `tool_fail`, xác nhận corpus hoạt động, rồi chạy lại workload.
- Owner: Pham Duc Anh
