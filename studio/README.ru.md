# Research & Design Studio

Рабочий конвейер для исследования, арт-дирекшна и выпуска редактируемых презентаций.
Дополняет существующую студию IntTrade, сохраняя Word/Excel, редактор текста,
Humanizer и проверяемый установщик OFL-шрифтов.

Шесть основных навыков находятся в `.agents/skills/`: evidence-first-research,
presentation-art-director, visual-document-studio, professional-writing-editor,
independent-quality-reviewer, workflow-reliability. Humanizer — отдельный
вспомогательный навык по явному запросу. Тела инструкций читаются по необходимости;
маршрутизация коротких заданий задана в корневом `AGENTS.md`.

```bash
# Из корня репозитория. Не переустанавливает исправные зависимости.
bash scripts/bootstrap.sh
python3 studio/scripts/studio.py new --id my-task --brief 'Задание'
python3 studio/scripts/acceptance.py --out work/acceptance
```

Для новой задачи нужно создать собственную структуру и макеты.
`build-demos.cjs` — проверка трёх разных брифов, а не универсальный шаблон.
Все коммерческие данные в примерах вымышленные и помечены на слайдах.

Проверенные примеры, PDF и протоколы: [examples/acceptance](examples/acceptance/).
Полный результат настройки: [IMPLEMENTATION.ru.md](IMPLEMENTATION.ru.md).
Существующие утилиты DOCX/XLSX остаются в корневом `scripts/`.

Состояние приёмки: **PARTIAL**. Технический конвейер и тест с намеренными ошибками
работают. Отдельный семантический/визуальный ревьюер не запускался; доступ к
изображениям дизайнерских портфолио ограничен; новая сессия ещё не проверяла
автоматический выбор навыков. Файлы конфигурации не публикуют окружение автоматически.
