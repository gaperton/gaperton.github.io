---
id: 5501
date: 2026-03-02T16:09:05+00:00
author: Andrey-Yamanov
author_handle: @tenphi
reply_to: 5499
---

Я в целом плюс минус базовые настройки использовал в LM Studio, ну контекстное окно увеличил до 128К. Заработало после смены Claude Code на Zed.

``````
"language_models": {
    "lmstudio": {
      "api_url": "http://localhost:1234/v1",
    },
  },

  "agent": {
    "default_model": {
      "provider": "lmstudio",
      "model": "qwen/qwen3.5-35b-a3b",
    },```
  },
```

конфиг Zed.

Пока успел отправить на Review здоровенного сложного pipeline'а. Нашел интересные проблемы неочевидные. Ща отправил фиксить, посмотрим, насколько хорошо у него это получится. Opus 4.6 потом ревью сделает и проверим качетсво работы 🙂