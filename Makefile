##
## EPITECH PROJECT, 2026
## Python Makefile
## File description:
## Makefile
##

NAME	=	3pf

SRC	=	./main.py

all:
	@python3 $(SRC)

install:
	@echo "\e[1mCreating virtual environment...\e[0m"
	@python3 -m venv venv > /dev/null
	@echo "\e[1mUpgrading virtual environment...\e[0m"
	@venv/bin/pip install --upgrade pip > /dev/null
	@echo "\e[1mInstalling Compiler...\e[0m"
	@venv/bin/pip install pyinstaller > /dev/null
	@echo "\e[1m\e[32mVirtual environment ready!\e[0m"

uninstall:
	@echo "\e[1mRemoving virtual environment...\e[0m"
	@rm -rf venv
	@echo "\e[1m\e[32mVirtual environment removed!\e[0m"

compile:
	@echo "\e[1mCompiling 3PF into binary...\e[0m"
	@(venv/bin/pyinstaller --log-level=WARN --onefile --name $(NAME) $(SRC) > /dev/null) \
		|| (echo "\e[31m\e[1mFailed to compile 3PF.\e[0m" && exit 1)
	@echo "\e[1m\e[32mCompiled successfully!\e[0m"
	@mv ./dist/$(NAME) .
	@rm -rf ./dist
	@rm -rf $(NAME).spec

clean:
	@echo "Removing build files"
	@rm -rf ./build

fclean: clean
	@echo "Removing binary"
	@rm -rf $(NAME)

re: fclean compile

