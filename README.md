# ТЗ

Условие.
Необходимо реализовать веб-приложение на Python для управления сетевыми интерфейсами локальной машины с установленной ОС Linux посредством команды ip addr. Фреймворк использовать на Ваш выбор (Django/Flask/FastAPI).
Приложение должно содержать следующий набор функционала. (Для веб, использовать можете любой фреймворк, или нативный JS):

- Авторизация пользователя
- Включение/выключение сетевого интерфейса
- Добавление IP адреса
- Удаление IP адреса
- Изменение IP адреса
- Изменение маски подсети

Разместить публичный проект с приложением на своём аккаунте Github. Приветствуется документация по развертке и эксплуатации Вашего приложения.

## Dependencies

Arch-based Linux distributions:

```bash
sudo pacman -S python python-pip python-virtualenv
```

Debian-based distributions:

```bash
sudo apt install python3 python3-pip python-virtualenv
```

Gentoo-based distributions:

```bash
sudo emerge --ask dev-lang/python dev-python/pip dev-python/virtualenv
```

RPM-based distributions:

```bash
sudo yum install -y python3 python-pip python-virtualenv
```

## Installation

```bash
git clone https://github.com/ozz-life/temp-flaskIPAddr
cd temp-flaskIPAddr/
cd backend/
python3 -m venv venv
. venv/bin/activate
pip install Flask
pip install python-dotenv
pip install flask-basicauth
```

## Starting

Запускать из под пользователя, имеющего необходимые права

```bash
./start.sh
```
