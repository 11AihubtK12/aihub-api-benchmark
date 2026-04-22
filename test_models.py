import requests
import time
import json

API_KEY = "API_KEY"
BASE_URL = "https://aihubapi.xyz/v1"

models = [
    "gpt-4o-mini",
    "gpt-4",
    "claude-3-haiku",
    "qwen-turbo",
    "doubao",
]

test_prompt = "Hello, reply a short sentence."

results = []

for model in models:
    print(f"Testing {model}...")
    start = time.time()

    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": test_prompt}],
                "temperature": 0.7
            },
            timeout=20
        )
        end = time.time()
        speed = round(end - start, 2)

        if resp.status_code == 200:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            results.append({
                "model": model,
                "status": "ok",
                "speed": speed,
                "content": content.strip()
            })
        else:
            results.append({
                "model": model,
                "status": f"error {resp.status_code}",
                "speed": speed
            })
    except Exception as e:
        results.append({
            "model": model,
            "status": "fail",
            "error": str(e)
        })

# 保存结果
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Done. Results saved to results.json")
