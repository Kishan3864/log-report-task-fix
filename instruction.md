There is an Apache-style access log at `/app/access.log`. Each line looks like:

```
192.168.0.1 - - [16/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
```

Analyze the log and write a JSON summary report to `/app/report.json`.

The report must be a single JSON object with exactly these keys:

- `total_requests` (integer): the number of non-empty lines in the log.
- `unique_ips` (integer): the number of distinct client IP addresses (the first field of each line).
- `top_path` (string): the request path that appears most often in the log (the path portion of the quoted request line, e.g. `/index.html`).

## Success criteria

1. The file `/app/report.json` exists and contains valid JSON.
2. The JSON is an object with exactly the keys `total_requests`, `unique_ips`, and `top_path`.
3. `total_requests` equals the number of non-empty lines in `/app/access.log`.
4. `unique_ips` equals the number of distinct IPs in `/app/access.log`.
5. `top_path` equals the most frequently requested path in `/app/access.log`.
