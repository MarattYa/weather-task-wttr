# Weather task

Скрипт получает текущую погоду для городов через API `wttr.in`, выводит
температуру и страну, а затем группирует результаты по странам.

Используются только модули стандартной библиотеки Python.

## Запуск

```bash
python weather_task.py Cities.txt
```

Чтобы дополнительно сохранить отчёт в файл:

```bash
python weather_task.py Cities.txt --output weather_results.txt
```

