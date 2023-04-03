### Hexlet tests and linter status:
[![Actions Status](https://github.com/Parrot7325/python-project-50/workflows/hexlet-check/badge.svg)](https://github.com/Parrot7325/python-project-50/actions)

### Code climate maintainability:
[![Maintainability](https://api.codeclimate.com/v1/badges/4a6da3eeda1f0e923fcd/maintainability)](https://codeclimate.com/github/Parrot7325/python-project-50/maintainability)

### Test Coverage:
[![Test Coverage](https://api.codeclimate.com/v1/badges/4a6da3eeda1f0e923fcd/test_coverage)](https://codeclimate.com/github/Parrot7325/python-project-50/test_coverage)

### Вычислитель отличий
Библиотека/инструмент командной строки для вычисления различий между двумя конфигурационными файлами (деревьями данных), работает с форматами json и yaml. Для вывода доступны три формата:
1) stylish (классическое дерево)
2) plain (текстовый)
3) json (выводит внутреннее представление библиотеки о различиях двух деревьев в формате json для передачи другим программам)

### Установка
Для установки потребуется python версии 3.9 или новее и poetry версии 1.2.2.
Для установки окружения выполните
```bash
make install
```
Для сборки пакета выполните
```bash
make build
```
Для установки пакета
```bash
make package-install
```
Или вместо всех трех команд
```bash
make retry
```

### Использование
```bash
gendiff [-h] [-f OUTPUT_FORMAT] first_file second_file

Compares two configuration files and shows a difference.

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f OUTPUT_FORMAT, --output_format OUTPUT_FORMAT
                        set format of output
```

### Демонстрации:
Вывод инструкции
[![asciicast](https://asciinema.org/a/YXKyVhceGo42eBHhvnx2gUTKM.svg)](https://asciinema.org/a/YXKyVhceGo42eBHhvnx2gUTKM)

Stylish (формат по умолчанию)
[![asciicast](https://asciinema.org/a/KK3GbZ4SoG6NBitOetYCOoB7t.svg)](https://asciinema.org/a/KK3GbZ4SoG6NBitOetYCOoB7t)

Plain (текстовый формат)
[![asciicast](https://asciinema.org/a/Fmn1tnILjlSgWUQOBMMaZfN7H.svg)](https://asciinema.org/a/Fmn1tnILjlSgWUQOBMMaZfN7H)

Формат json
[![asciicast](https://asciinema.org/a/mrbgEIG4qkE20JnDJUu1nROYe.svg)](https://asciinema.org/a/mrbgEIG4qkE20JnDJUu1nROYe)
