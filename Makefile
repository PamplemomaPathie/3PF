##
## EPITECH PROJECT, 2026
## Python Makefile
## File description:
## Makefile
##

NAME	=	3pf

BASEDIR	=	~/.3pf

SRC	=	./main.py

SHELL := /bin/bash


all:
	@echo -e "\e[1mWelcome to 3pf!\e[0m\nPlease use 'make install' to install 3pf."

install:
	@bash ./install.sh || \
	    (echo -e "\e[1mLaunching compilation...\e[0m" && \
	    make --no-print-directory init && \
	    make --no-print-directory compile && \
	    bash ./install.sh)

uninstall:
	@echo -e "\e[1mUninstalling 3pf.\e[0m"
	@make --no-print-directory fclean
	@echo -e "Removing all libraries."
	@rm -rf $(BASEDIR)
	@read -p "Do you want to remove the persistence? (y/n) " answer; \
	if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
		sudo rm -rf /etc/bash_completion.d/3pf; \
	fi
	@echo -e "\e[1m\e[32mSuccessfully removed 3pf!\e[0m"

init:
	@echo -e "\e[1mCreating virtual environment...\e[0m"
	@python3 -m venv venv > /dev/null
	@echo -e "\e[1mUpgrading virtual environment...\e[0m"
	@venv/bin/pip install --upgrade pip > /dev/null
	@echo -e "\e[1mInstalling Compiler...\e[0m"
	@venv/bin/pip install pyinstaller > /dev/null
	@echo -e "\e[1m\e[32mVirtual environment ready!\e[0m"

remove:
	@echo -e "\e[1mRemoving virtual environment...\e[0m"
	@rm -rf venv
	@echo -e "\e[1m\e[32mVirtual environment removed!\e[0m"

compile:
	@echo -e "\e[1mCompiling 3PF into binary...\e[0m"
	@([[ -d ./venv ]] && [[ -f venv/bin/pyinstaller ]]) \
	  || (echo -e "\e[31m\e[1mPlease init virtual environment before compiling\e[0m" && exit 1)
	@(venv/bin/pyinstaller --log-level=WARN --onefile --name $(NAME) $(SRC) > /dev/null) \
		|| (echo -e "\e[31m\e[1mFailed to compile 3PF.\e[0m" && exit 1)
	@echo -e "\e[1m\e[32mCompiled successfully!\e[0m"
	@mv ./dist/$(NAME) .
	@rm -rf ./dist
	@rm -rf $(NAME).spec

clean	:
	@echo -e "Removing build files"
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./3pf_config.bash

fclean: clean remove
	@rm -rf $(NAME)

re: fclean compile

	
