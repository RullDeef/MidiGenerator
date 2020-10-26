
.PHONY : ML rgen

no :
	@echo ML or rgen

ML :
	@py ML/creator.py

rgen :
	@py Rgen/main.py
