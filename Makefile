reformat:
	isort apiiot clienteMqtt crud telegrambot && black --line-length=88 apiiot clienteMqtt crud telegrambot

black:
	black --check --diff --line-length=88 apiiot clienteMqtt crud telegrambot

#flake8:
#flake8 --config .flake8 http_retriever

code-quality:
	make reformat black

up:
	docker-compose -f docker-compose.yml up --build -d $(c)

login-mariadb:
	docker-compose -f docker-compose.yml exec mariadb bash -c "mysql -u root -proot 'sensores_remotos'"