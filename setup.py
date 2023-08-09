import setuptools

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
	long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
requirements = ['fuzzywuzzy==0.18.0',
                'Levenshtein==0.21.1',
                'pyreadline3==3.4.1',
                'python-Levenshtein==0.21.1',
                'rapidfuzz==3.1.1',
                'rich==13.5.2']

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
	# Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
	name="assistant_ostap",
	# Номер версии вашего пакета. Обычно используется семантическое управление версиями.
	version="0.0.20",
	# Имя автора.
	author="GoIt Team 3",
	# Его почта.
	author_email="",
	# Краткое описание, которое будет показано на странице PyPi.
	description="Your personal assistant Ostap",
	# Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
	long_description=long_description,
	# Определяет тип контента, используемый в long_description.
	long_description_content_type="text/markdown",
	# URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
	url="https://github.com/NeverInMind/Project_Team3/",
	# Находит все пакеты внутри проекта и объединяет их в дистрибутив.
	packages=setuptools.find_packages(),
	# requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
	install_requires=requirements,
	# Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.6',
	include_package_data=True,
    entry_points={'console_scripts': ['Ostap = assistant_ostap.main:main']}
)